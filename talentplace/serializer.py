from rest_framework import serializers
from .models import User
from .models import Rol
from .models import Category
from .models import Service
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import HiredService

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #Serializar campos del modelo (id, name, lastname,...)
        #Convertir datos del front en json antes de guardarlos en DB
        model = User
        fields = "__all__"
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        public_fields = {
            "email": data.get("email"),
            "username": data.get("username"),
            "name": data.get("name"),
            "lastname": data.get("lastname"),
            "rol_id": data.get("rol_id"),
        }
        return public_fields

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
        
class HiredServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HiredService
        fields = "__all__"

class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.name
        token['lastname'] = user.lastname
        token['email'] = user.email
        token['rol'] = user.rol.id_rol
        return token