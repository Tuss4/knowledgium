from django.db import models
from django.contrib.auth.models import AbstractBaseUser


from .managers import CoderManager


class Coder(AbstractBaseUser):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    created = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CoderManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        if self.first_name and self.last_name:
            return '{0} {1}'.format(self.first_name, self.last_name)
        return self.get_short_name()

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.get_short_name()

    @property
    def is_staff(self):
        return self.is_admin
