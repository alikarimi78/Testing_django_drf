from django.db import models

# Create your models here.

# models.py

from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomToken(models.Model):
    user = models.ForeignKey(AbstractUser, on_delete=models.CASCADE)
    token = models.TextField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
