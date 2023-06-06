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

class User(models.Model):
    id_user = models.AutoField(primary_key = True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    birthdate = models.DateField()
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=11)
    email = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    rol = models.ForeignKey(Rol , on_delete=models.CASCADE)

    def __str__(self):
        return self.id_user
    
class Service(models.Model):
    id_service = models.AutoField(primary_key = True)
    offerer_id = models.ForeignKey(User , on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    service_name = models.CharField(max_length = 50)
    description = models.CharField(max_length = 200)
    price = models.FloatField()
    evidence_img = models.TextField(blank=True)
    evidence_video = models.TextField(blank=True)
    average_rating = models.IntegerField(blank=True, null=True)
    available = models.BooleanField(default=True)
    
    def __str__(self):
        return self.service_name

class HiredService(models.Model):
    id_hired_service = models.AutoField(primary_key = True)
    applicant_id = models.ForeignKey(User , on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service , on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)
    request_date = models.DateField()
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.service_id.average_rating = HiredService.objects.filter(service_id=self.service_id).aggregate(models.Avg('rating'))['rating__avg']
        self.service_id.save()

    def __str__(self):
        return self.id_hired_service
