import re

import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from phonenumbers import country_code_for_region


@deconstructible
class PhoneValidator:
    requires_context = False

    @staticmethod
    def clean(value, country_code=None):
        value = re.sub('[^0-9]+', '', value)

        if isinstance(country_code, str):
            n = country_code_for_region(country_code.upper())
            if n != 0:
                value = f"{n}{value}"

        if len(value) == 9:
            value = f"998{value}"

        return value

    @staticmethod
    def validate(value):
        try:
            z = phonenumbers.parse("+" + value)
            if not phonenumbers.is_valid_number(z):
                return False
        except:
            return False

        # if len(value) != 12 or not value.startswith("998"):
        #     return False

        return True

    @staticmethod
    def format(value):
        try:
            z = phonenumbers.parse("+" + value)
            if not phonenumbers.is_valid_number(z):
                return value

            return phonenumbers.format_number(z, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except:
            return value

    def __call__(self, value):
        if not PhoneValidator.validate(value):
            raise ValidationError("Kiritilgan qiymat telefon raqam emas")

