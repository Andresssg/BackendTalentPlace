from django.db import models

# Create your models here.
class Rol(models.Model):
    id_rol = models.AutoField(primary_key = True)
    rol_name = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.rol_name
    
class Category(models.Model):
    id_category = models.AutoField(primary_key = True)
    category_name = models.CharField(max_length = 75)

    def __str__(self):
        return self.category_name

class Service(models.Model):
    id_service = models.AutoField(primary_key = True)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    service_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    evidence_img = models.TextField(blank=True)
    evidence_video = models.TextField(blank=True)
    
    def __str__(self):
        return self.service_name

class User(models.Model):
    id_user = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol , on_delete=models.CASCADE)

    def __str__(self):
        return self.id_user
    
class OfferedService(models.Model):
    id_offered_service = models.AutoField(primary_key = True)
    service_id = models.ForeignKey(Service , on_delete=models.CASCADE)
    offerer_id = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return self.id_offered_service

class HiredService(models.Model):
    id_hired_service = models.AutoField(primary_key = True)
    applicant_id = models.ForeignKey(User , on_delete=models.CASCADE)
    offered_service_id = models.ForeignKey(OfferedService , on_delete=models.CASCADE)
    price = models.FloatField()
    request_date = models.DateField()
    
    def __str__(self):
        return self.id_hired_service
