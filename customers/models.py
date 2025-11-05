import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class Customer(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name']
    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name
