from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        #Serializar campos del modelo (id, name, lastname,...)
        #Convertir datos del front en json antes de guardarlos en DB
        model = User
        fields = "__all__"