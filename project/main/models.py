from django.db import models

# Create your models here.

class User(models.Model):
    key = models.CharField(max_length=500)
    date_create = models.DateField()