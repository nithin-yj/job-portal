from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):

    class Role(models.TextChoices):
        EMPLOYEE = 'EMPLOYEE', 'Employee'
        EMPLOYER = 'EMPLOYER', 'Employer'

    username = None

    email = models.EmailField(unique=True)

    role = models.CharField(
        max_length=10,
        choices=Role.choices
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email