from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Permission

from user.models import User

admin.site.register(Permission)


@admin.register(User)
class UserAdmin1(UserAdmin):
    pass
