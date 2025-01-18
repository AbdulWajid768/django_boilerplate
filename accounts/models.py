"""Models for accounts app."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    """Custom user manager for using email instead of username."""

    def create_user(self, email, password=None, **kwargs):
        """Create user with given params."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_staff(self, email, password=None, **kwargs):
        """Create staff user with given params."""
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = user.is_active = True
        user.save(update_fields=['is_staff', 'is_active'])

        return user

    def create_superuser(self, email, password=None, **kwargs):
        """Create superuser with given params."""
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = user.is_superuser = user.is_active = True
        user.save(update_fields=['is_staff', 'is_superuser', 'is_active'])

        return user


class User(AbstractUser):
    """Custom user model for custom settings."""

    username = None
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
