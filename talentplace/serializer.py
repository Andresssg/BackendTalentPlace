from rest_framework import serializers
from .models import User
from .models import Rol
from .models import Category
from .models import Service
from .models import HiredService
from .models import OfferedService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #Serializar campos del modelo (id, name, lastname,...)
        #Convertir datos del front en json antes de guardarlos en DB
        model = User
        fields = "__all__"

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class RolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rol
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = "__all__"

class OfferedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferedService
        fields = "__all__"
        
class HiredServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiredService
        fields = "__all__"