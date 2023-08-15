from django.db import models
from django.contrib.auth.models import AbstractUser, Group
import hashlib

# Create your models here.


class user_details(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    USERNAME_FIELD = "email"

    groups = models.ManyToManyField(
        Group, related_name="custom_user_groups", blank=True
    )

    user_permissions = models.ManyToManyField(
        Group, related_name="custom_user_permissions", blank=True
    )
