from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueTogetherValidator

from serializers.validation_service import DynamicRequestFieldService, CheckConditionValidationService


class UniqueTogetherDynamicRequestFieldsConstraintValidator(UniqueTogetherValidator):

    def __init__(self, queryset, fields, serializer, dynamic_fields=None):
        self.dynamic_request_field_service = DynamicRequestFieldService(
            serializer.context['request'], serializer.dynamic_request_fields
        )
        self.dynamic_fields = dynamic_fields or []
        super().__init__(queryset, fields)

    def __call__(self, attrs, serializer):
        for dynamic_field in self.dynamic_fields:
            attrs[dynamic_field] = self.dynamic_request_field_service.get_value(dynamic_field)
        try:
            super().__call__(attrs, serializer)
        except ValidationError:
            # This except is only to return a more accurate message that also includes dynamic fields.
            # Copied from super method call.
            field_names = ', '.join(self.fields + tuple(self.dynamic_fields))
            message = self.message.format(field_names=field_names)
            raise ValidationError(message, code='unique')


class UniqueTogetherConstraintValidator(UniqueTogetherDynamicRequestFieldsConstraintValidator):

    def __init__(self, queryset, fields, serializer, condition, dynamic_fields=None):
        self.condition = condition
        self.serializer = serializer
        super().__init__(queryset, fields, serializer, dynamic_fields)

    def filter_queryset(self, attrs, queryset, serializer):
        queryset = queryset.filter(self.condition)
        if self.condition:
            queryset = queryset.filter(self.condition)
        return super().filter_queryset(attrs, queryset, serializer)

    def __call__(self, attrs, serializer):
        service = CheckConditionValidationService(self.condition, self.serializer, attrs)
        if service.validate():
            super().__call__(attrs, serializer)


class CheckConstraintValidator:

    def __init__(self, constraint, serializer):
        self.serializer = serializer
        self.constraint = constraint
        self.requires_context = True

    def __call__(self, attrs, serializer):
        service = CheckConditionValidationService(self.constraint.check, self.serializer, attrs)
        check = service.validate()
        if not check:
            raise ValidationError(f'Check constraint failed with name: {self.constraint.name}', code='check_constraint')
