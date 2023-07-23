import uuid

from django.db import models
from django.contrib.auth.models import User


class UserToken(models.Model):
    owner = models.ForeignKey(User, models.CASCADE, related_query_name="user")
    token = models.CharField(default=uuid.uuid4(), unique=True, max_length=1024)

    class Meta:
        verbose_name = "User token"
        verbose_name_plural = "Users token"
