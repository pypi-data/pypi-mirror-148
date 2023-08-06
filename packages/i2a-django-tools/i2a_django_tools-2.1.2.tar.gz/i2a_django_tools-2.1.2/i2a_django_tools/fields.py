from django.core import validators
from django.db import models
from django.utils.functional import cached_property


class AmountField(models.DecimalField):

    def __init__(self, *, max_digits=12, decimal_places=2, **kwargs):
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, **kwargs
        )

    @cached_property
    def validators(self):
        return super().validators + [
            validators.MinValueValidator(0)
        ]


class PercentField(models.DecimalField):

    def __init__(self, *, max_digits=12, decimal_places=2, **kwargs):
        super().__init__(
            max_digits=max_digits, decimal_places=decimal_places, **kwargs
        )

    @cached_property
    def validators(self):
        return super().validators + [
            validators.MinValueValidator(0),
            validators.MaxValueValidator(1),
        ]


class PhoneNumberField(models.CharField):

    def __init__(self, *, max_length=16, **kwargs):
        super().__init__(
            max_length=16, **kwargs
        )

    @cached_property
    def validators(self):
        return super().validators + [
            validators.MinLengthValidator(9),
        ]

    def clean(self, value: str, model_instance):
        super().clean(value, model_instance)
        return value.replace(" ", "")
