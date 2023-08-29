from django import db
from django.contrib.auth import models
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class CustomUser(models.AbstractUser):
    # telephone = PhoneNumberField(null=False, blank=False, unique=True)
    pass
