from django.conf import settings
from django.db import models


# Create your models here.

class Product(models.Model):
    """
    Create the Product table to stock and use user's saved products
    """
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    ng = models.CharField(max_length=1)
    img = models.URLField(null=True)
    link_off = models.URLField()
    energy = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    fat = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    saturated_fat = models.DecimalField(max_digits=6, decimal_places=4,
                                        null=True)
    carbohydrate = models.DecimalField(max_digits=6, decimal_places=4,
                                       null=True)
    sugars = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    proteins = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    salt = models.DecimalField(max_digits=6, decimal_places=4, null=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="products")
