"""Models for accounts app: custom email-based User and Client profile."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from common.mixins import TimeStampMixin, UUIDPKMixin


class CustomUserManager(BaseUserManager):
    """Custom user manager that uses email as the unique identifier."""

    def create_user(self, email, password=None, **kwargs):
        """Create and return a regular user with the given email and password."""
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_staff(self, email, password=None, **kwargs):
        """Create and return a staff user."""
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = user.is_active = True
        user.save(update_fields=['is_staff', 'is_active'])
        return user

    def create_superuser(self, email, password=None, **kwargs):
        """Create and return a superuser."""
        user = self.create_user(email=email, password=password, **kwargs)
        user.is_staff = user.is_superuser = user.is_active = True
        user.save(update_fields=['is_staff', 'is_superuser', 'is_active'])
        return user


class User(AbstractUser):
    """Custom user model that uses email instead of username."""

    username = None
    email = models.EmailField(verbose_name='email', max_length=100, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        """Return the user's email as the human-readable identifier."""
        return f'{self.email}'


class Client(UUIDPKMixin, TimeStampMixin):
    """Client profile attached one-to-one to a User, populated on first Google sign-in."""

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='client',
    )
    phone = models.CharField(max_length=20, blank=True)
    google_id = models.CharField(max_length=100, blank=True)
    profile_complete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'

    def __str__(self):
        """Return the underlying user's email for admin readability."""
        return f'{self.user.email}'
