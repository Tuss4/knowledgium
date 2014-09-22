from django.contrib.auth.models import BaseUserManager


class CoderManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)
        if 'first_name' in kwargs:
            user.first_name = kwargs['first_name']
        if 'last_name' in kwargs:
            user.last_name = kwargs['last_name']
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_admin = True
        user.save(using=self._db)
        return user
