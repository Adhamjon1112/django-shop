from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from config.validators import PhoneValidator


class ShopUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        username = PhoneValidator.clean(username)

        if not username:
            raise ValueError("Username kiritilmagan")

        if not PhoneValidator.validate(username):
            raise ValueError("Kiritilgan qiymat telefon raqam emas")

        user = self.model(
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    objects = ShopUserManager()

    username = models.CharField(
        _("username"),
        max_length=16,
        unique=True,
        help_text=_(
            "Required. Telefon raqam"
        ),
        validators=[PhoneValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )

    REQUIRED_FIELDS = []
