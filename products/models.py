from django.db import models

# Create your models here.
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=500, blank=True, null=True)
    udf1 = models.CharField(max_length=10, blank=True, null=True)
    udf2 = models.CharField(max_length=10, blank=True, null=True)
    udf3 = models.CharField(max_length=10, blank=True, null=True)