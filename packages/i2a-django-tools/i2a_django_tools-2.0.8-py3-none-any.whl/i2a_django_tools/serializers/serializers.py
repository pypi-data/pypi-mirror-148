from django.core.exceptions import ObjectDoesNotExist
from django.utils.duration import duration_iso_string
from django.db.models import DurationField
from dotmap import DotMap
from rest_framework.fields import DecimalField, Field
from enumfields.drf import EnumSupportSerializerMixin
from timezone_field import TimeZoneField
from i2a_django_tools import fields
from collections import defaultdict, OrderedDict

from django.db.models import CheckConstraint, UniqueConstraint
from rest_framework import serializers
from rest_framework.fields import empty

from i2a_django_tools.serializers.validation_service import DynamicContextFieldService
from i2a_django_tools.serializers.validators import CheckConstraintValidator, UniqueTogetherConstraintValidator, \
    UniqueTogetherDynamicRequestFieldsConstraintValidator


class BaseModelSerializer(EnumSupportSerializerMixin, serializers.ModelSerializer):
    """
            ModelSerializer with additional CheckConstraintValidator, UniqueConstraintValidator and UniqueTogetherValidator
                with dynamic serializer fields provided by context (request)

            Also adds dynamic fields to model object, while calling method .save(), when override_save = True

            In serializer Meta class specify 'dynamic_context_fields' field, if you want to get
                serializer fields from request. It is a dict with key 'field' and value 'path' to value in request e.g:
                    dynamic_context_fields = {
                        'user_profile': 'request.user.user_profile'
                    }
        """

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.override_save = DotMap(getattr(self.Meta, 'override_save', False))
        self.dynamic_context_fields = getattr(self.Meta, 'dynamic_context_fields', {})
        self.model_class_inheritance_tree = ([self.Meta.model] + list(self.Meta.model._meta.parents))
        self.source_map = self.get_source_map()

    def save(self, **kwargs):
        if self.override_save:
            service = DynamicContextFieldService(self.context, self.dynamic_context_fields)
            for dynamic_context_field in self.dynamic_context_fields:
                kwargs[dynamic_context_field] = service.get_value(dynamic_context_field)
        return super().save(**kwargs)

    def get_validators(self):
        validators = super().get_validators()
        return self.get_constraint_validators() + self.get_context_fields_unique_together_validators() + validators

    def get_constraint_validators(self):
        validators = []
        # Register constraints validators
        for parent_class in self.model_class_inheritance_tree:
            for constraint in parent_class._meta.constraints:
                if isinstance(constraint, CheckConstraint):
                    # CheckConstraint validator
                    validators.append(CheckConstraintValidator(
                        constraint, serializer=self
                    ))
                if isinstance(constraint, UniqueConstraint):
                    # UniqueConstraint validator
                    field_names, dynamic_field_names = self.get_field_dynamic_names(constraint.fields)
                    validator = UniqueTogetherConstraintValidator(
                        queryset=parent_class._default_manager,
                        fields=field_names,
                        serializer=self,
                        dynamic_fields=dynamic_field_names,
                        condition=constraint.condition
                    )
                    validators.append(validator)
        return validators

    def get_context_fields_unique_together_validators(self):
        """
            Register unique together validators with dynamic fields from request. By default, rest_framework
                UniqueTogetherValidator ignores that unique_together constrains where at least
                    one field is fetched dynamically, not from initial serializer data, but e.g. from request.
        """
        validators = []
        for parent_class in self.model_class_inheritance_tree:
            for unique_together in parent_class._meta.unique_together:
                if not set(self.source_map).issuperset(unique_together):
                    field_names, dynamic_field_names = self.get_field_dynamic_names(unique_together)
                    validator = UniqueTogetherDynamicRequestFieldsConstraintValidator(
                        queryset=parent_class._default_manager,
                        fields=field_names,
                        serializer=self,
                        dynamic_fields=dynamic_field_names,
                    )
                    validators.append(validator)
        return validators

    def get_field_dynamic_names(self, unique_together):
        dynamic_field_names = set(unique_together).difference(set(self.source_map))
        # Get field_names of fields that are not dynamic, but by default on the serializer
        field_names = tuple(self.source_map[f][0] for f in set(unique_together).difference(dynamic_field_names))
        return field_names, dynamic_field_names

    def get_source_map(self):
        """
            This block of code is copied from rest_framework.BaseModelSerializer.get_unique_together_validators
            It returns all fields available on the serializer from which is possible to get a value.
        """
        field_sources = OrderedDict(
            (field.field_name, field.source) for field in self._writable_fields
            if (field.source != '*') and ('.' not in field.source)
        )
        field_sources.update(OrderedDict(
            (field.field_name, field.source) for field in self.fields.values()
            if field.read_only and (field.default != empty) and (field.source != '*') and ('.' not in field.source)
        ))
        source_map = defaultdict(list)
        for name, source in field_sources.items():
            source_map[source].append(name)
        return source_map


class FilteredByPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Just like PrimaryKeyRelatedField, but also filters the queryset by account_id
    taken from request. Other values to filter by might be specified by using
    `extra_dynamic_lookup_fields`, but they need to correspond to variables
    on the request object.

    param extra_dynamic_query_filter_expressions - List of Q methods that take the request parameter
        and return the Q expression.

    fail_silently: when True, objects that don't exist in the db are returned as None
    """

    def __init__(
            self,
            lookup_field="pk",
            repr_field="pk",
            extra_dynamic_lookup_fields: dict = None,
            extra_dynamic_query_filter_expressions: list = None,
            fail_silently=False,
            distinct=False,
            *args,
            **kwargs,
    ):
        self.lookup_field = lookup_field
        self.extra_dynamic_lookup_fields = extra_dynamic_lookup_fields
        self.extra_dynamic_query_filter_expressions = extra_dynamic_query_filter_expressions
        self.repr_field = repr_field
        self.fail_silently = fail_silently
        self.distinct = distinct
        if self.lookup_field != "pk":
            self.default_error_messages[
                "does_not_exist"
            ] = f"Invalid {self.lookup_field} {{pk_value}} - object does not exist."
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        request = self.context.get("request", None)
        queryset = super().get_queryset()
        if not request:
            return queryset.none()
        dynamic_lookup = {}

        if self.extra_dynamic_lookup_fields:
            for path, value in self.extra_dynamic_lookup_fields.items():
                assert hasattr(request, value)
                dynamic_lookup[path] = getattr(request, value)
        qs = queryset.filter(**dynamic_lookup)

        if self.extra_dynamic_query_filter_expressions:
            for expression in self.extra_dynamic_query_filter_expressions:
                qs = qs.filter(expression(request))
        if self.distinct:
            qs = qs.distinct()
        return qs

    def to_internal_value(self, data):
        if self.pk_field is not None:
            data = self.pk_field.to_internal_value(data)
        try:
            return self.get_queryset().get(**{self.lookup_field: data})
        except ObjectDoesNotExist:
            if not self.fail_silently:
                self.fail("does_not_exist", pk_value=data)
            return None
        except (TypeError, ValueError):
            self.fail("incorrect_type", data_type=type(data).__name__)

    def use_pk_only_optimization(self):
        if self.repr_field == "pk":
            return True
        return False

    def to_representation(self, value):
        field = getattr(value, self.repr_field)
        if self.pk_field is not None:
            return self.pk_field.to_representation(field)
        return field


class AmountField(DecimalField):

    def __init__(
        self, *, max_digits=12, decimal_places=2, min_value=0, **kwargs
    ):
        super().__init__(
            decimal_places=decimal_places, max_digits=max_digits,
            min_value=min_value,
            **kwargs
        )


class PercentField(DecimalField):

    def __init__(
        self, *, max_digits=12, decimal_places=2, min_value=0, max_value=1,
        **kwargs
    ):
        super().__init__(
            decimal_places=decimal_places, max_digits=max_digits,
            min_value=min_value, max_value=max_value,
            **kwargs
        )


class IntEnumToStringField(Field):

    def __init__(self, enum, *args, **kwargs):
        self.enum = enum
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return self.enum(value).label


class ISODurationField(DurationField):

    def to_representation(self, value):
        return duration_iso_string(value)


class EnhancedModelSerializer(BaseModelSerializer):
    serializer_field_mapping = {
        **serializers.ModelSerializer.serializer_field_mapping,
        **{
            fields.AmountField: AmountField,
            fields.PercentField: PercentField,
            TimeZoneField: serializers.CharField,
            DurationField: ISODurationField,
        }
    }
