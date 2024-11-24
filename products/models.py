from django.db import models
from django.conf import settings

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Corrected
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Corrected
    image4 = models.ImageField(upload_to='product_images/', blank=True, null=True)  # Corrected

    def __str__(self):
        return self.name


# Cart model
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart item for {self.user.username} - {self.product.name}"
