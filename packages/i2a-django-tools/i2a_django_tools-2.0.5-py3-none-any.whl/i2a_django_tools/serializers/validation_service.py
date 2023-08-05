from django.db.models import Q

from serializers.expression_methods_mapping import FIELD_LOOKUP_EXPRESSION_METHODS, METHOD_EXPRESSION_METHODS


class DynamicRequestFieldService:
    """
        Method 'get_value' returns specific object, provided by value of 'dynamic_request_fields' dict parameter e.g:
            dynamic_request_fields = {
                'user_profile': 'request.user.user_profile'
            }
        Returns -> objects that equal self.request.user.user_profile
    """

    def __init__(self, request, dynamic_request_fields):
        self.dynamic_request_fields = dynamic_request_fields
        self.request = request

    def get_value(self, field):
        current_object = self
        for step in self.dynamic_request_fields[field].split('.'):
            current_object = getattr(current_object, step, None)
            if not current_object:
                # Should we raise some error if there is no path in request?
                return None
        return current_object

    def has_value(self, field):
        return field in self.dynamic_request_fields


class SerializerDynamicDataService:

    def __init__(self, serializer, source_attrs):
        self.serializer = serializer
        self.source_attrs = source_attrs
        self.initial_data = serializer.initial_data
        self.dynamic_request_field_service = DynamicRequestFieldService(
            serializer.context['request'], serializer.dynamic_request_fields or []
        )

    def get_field_value(self, field):
        if not self.dynamic_request_field_service.has_value(field):
            return self.initial_data.get(field) or self.source_attrs.get(field)
        return self.dynamic_request_field_service.get_value(field)


class CheckConditionValidationService:
    """
        Method 'validate' checks if serializer data meets the sql query condition, without calling query on database.
        Also using dynamic fields from request, provided by 'dynamic_request_fields' e.g:
            dynamic_request_fields = {
                'user_profile': 'request.user.user_profile'
            }
        source_attrs -> additional values that are fetched from RelatedField under parameter called 'source'
    """

    def __init__(self, condition: Q, serializer: 'BaseModelSerializer', source_attrs=None):
        self.condition = condition
        self.serializer_dynamic_data_service = SerializerDynamicDataService(serializer, source_attrs or {})

    def validate(self):
        return self.validate_check_condition(self.condition)

    def validate_check_condition(self, current_check):
        connector = current_check.connector
        expression_values = []
        for child in current_check.children:
            if isinstance(child, tuple):
                # Terminal expression e.g: name__isnull=False
                expression_value = self.evaluate_expression(*child)
            else:
                # Nested Q expression e.g: Q(Q(...) | Q(...))
                expression_value = self.validate_check_condition(child)
            expression_values.append(expression_value)

        if not expression_values:
            raise ValueError(f'Variable expression_values is empty for check: {str(current_check)}')
        is_valid = any(expression_values) if connector == 'OR' else all(expression_values)
        # This is XOR \/
        return (is_valid and not current_check.negated) or (current_check.negated and not is_valid)

    def evaluate_expression(self, expression, value):
        value = self.get_expression_value(value)
        expression_parts = expression.split('__')
        field = expression_parts[0]
        field_value = self.serializer_dynamic_data_service.get_field_value(field)

        field_expression = 'exact'
        if len(expression_parts) == 2:
            field_expression = expression_parts[1]
        return FIELD_LOOKUP_EXPRESSION_METHODS[field_expression](field_value, value)

    def get_expression_value(self, value):
        expression_method = METHOD_EXPRESSION_METHODS.get(value.__class__)
        if expression_method:
            return expression_method(value, self)
        return value
