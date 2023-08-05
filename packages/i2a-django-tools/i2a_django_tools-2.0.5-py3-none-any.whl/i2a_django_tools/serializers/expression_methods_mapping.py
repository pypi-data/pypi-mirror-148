from django.db.models import F
from django.db.models.expressions import CombinedExpression

FIELD_LOOKUP_EXPRESSION_METHODS = {}
METHOD_EXPRESSION_METHODS = {}
MATH_EXPRESSION_METHODS = {}


"""
    Register lookup / expression that are used in 'constraints' Meta class property on serializer.ModelSerializer e.g:
        models.CheckConstraint(
            check=(
                    Q(user_profile__isnull=False) &
                    Q(sum=F('left') + F('right'))
            ),
        )
    In the above example: 
        lookup expression -> __isnull
        method expression -> F
        math expression -> +
    
    WARNING!!! When register method expression remember about recursive method calls.
"""


def register_lookup_expression(lookup=None):
    def decorator(func):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        FIELD_LOOKUP_EXPRESSION_METHODS[lookup] = func
        return wrapped
    return decorator


def register_method_expression(expression=None):
    def decorator(func):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        METHOD_EXPRESSION_METHODS[expression] = func
        return wrapped
    return decorator


def register_math_expression(math_expression=None):
    def decorator(func):
        def wrapped(*args, **kwargs):
            return func(*args, **kwargs)
        MATH_EXPRESSION_METHODS[math_expression] = func
        return wrapped
    return decorator


"""
    Method expressions
"""


@register_method_expression(F)
def field_expression(value, condition_service: 'CheckConditionValidationService'):
    return condition_service.serializer_dynamic_data_service.get_field_value(value.name)


@register_method_expression(CombinedExpression)
def combined_expression(value, condition_service: 'CheckConditionValidationService'):
    # Lhs/Rhs is left and right side of a combined expression
    left_value = condition_service.get_expression_value(value.lhs)
    right_value = condition_service.get_expression_value(value.rhs)
    return MATH_EXPRESSION_METHODS[value.connector](left_value, right_value)


"""
    Lookup expressions
"""


@register_lookup_expression(lookup="exact")
def exact_expression(field_value, value) -> bool:
    return field_value == value


@register_lookup_expression(lookup="isnull")
def is_null_expression(field_value, value) -> bool:
    # Value means if field must be null or not e.g: user_profile__isnull=True
    return (field_value is None) if value else (field_value is not None)


@register_lookup_expression(lookup="gt")
def gt_expression(field_value, value) -> bool:
    return field_value > value


@register_lookup_expression(lookup="gte")
def gte_expression(field_value, value) -> bool:
    return field_value >= value


@register_lookup_expression(lookup="lt")
def lt_expression(field_value, value) -> bool:
    return field_value < value


@register_lookup_expression(lookup="lte")
def lte_expression(field_value, value) -> bool:
    return field_value <= value


@register_lookup_expression(lookup="in")
def in_expression(field_value, value) -> bool:
    if isinstance(value, (tuple, list)):
        return field_value in value
    return field_value == value


"""
    Math expressions
"""


@register_math_expression(math_expression='+')
def add_expression(value_1, value_2):
    return value_1 + value_2


@register_math_expression(math_expression='-')
def add_expression(value_1, value_2):
    return value_1 - value_2


@register_math_expression(math_expression='/')
def add_expression(value_1, value_2):
    return value_1 / value_2


@register_math_expression(math_expression='*')
def add_expression(value_1, value_2):
    return value_1 * value_2


@register_math_expression(math_expression='%')
def add_expression(value_1, value_2):
    return value_1 % value_2


@register_math_expression(math_expression='^')
def add_expression(value_1, value_2):
    return value_1 ^ value_2
