from django.db import models

# Create your models here.
class book(models.Model):
    name = models.CharField(blank=True,max_length=20)
    age = models.CharField(blank=True,max_length=20)
    gender = models.CharField(blank=True,max_length=20)
    address = models.CharField(blank=True,max_length=20)