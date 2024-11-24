
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    contact_no = models.CharField(max_length=10, null=True)
    gender = models.CharField(max_length=10, null=True)
    date_of_birth = models.DateField(null=True)
    residential_address = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    district = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, null=True, unique=True)
    udf1 = models.CharField(max_length=10, blank=True, null=True)
    udf2 = models.CharField(max_length=10, blank=True, null=True)
    udf3 = models.CharField(max_length=10, blank=True, null=True)