from django.db import models

# Create your models here.


class Product(models.Model):

    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField(blank=False, null=False)


class CompleteProduct(models.Model):

    complete_title = models.CharField(max_length=100, blank=True, null=True)
    the_product = models.ForeignKey(Product, on_delete=models.CASCADE)
