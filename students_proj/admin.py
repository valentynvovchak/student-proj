# назвали admin.py,оскільки він міститиме кастомний клас адміністрації User моделі.
# Завдяки імені модуля admin.py Django фреймворк автоматично підчепить усі зміни.

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import User

from .models import StudentProfile


class StudentProfileInline(admin.StackedInline):
    model = StudentProfile


class UserAdmin(auth_admin.UserAdmin):
    inlines = (StudentProfileInline,)


# replace existing User admin form
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
