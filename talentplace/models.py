from django.db import models

# Create your models here.
class Rol(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.name

class User(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol , on_delete=models.CASCADE)

    def __str__(self):
        return self.id
    
class Category(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 75)

    def __str__(self):
        return self.name
