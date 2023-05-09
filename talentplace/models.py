from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.CharField(max_length=11)
