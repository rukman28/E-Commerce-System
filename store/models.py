from django.db import models

class Product(models.Model):
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  image = models.ImageField(upload_to='products/')

  def __str__(self):
    return self.title

class ProductCategory(models.Model):
  name = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  products = models.ManyToManyField(Product, related_name='categories')

  def __str__(self):
    return self.name