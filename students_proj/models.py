from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class StudentProfile(models.Model):
    """To keep extra user data"""
    # user mapping
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    # extra user data
    mobile_phone = models.CharField(max_length=12, blank=True, verbose_name=_('Телефон'), default='')

    class Meta(object):
        verbose_name = _('Профіль Користувача')

    def __str__(self):
        return self.user.username
