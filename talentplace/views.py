from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserSerializer
from .serializer import RolSerializer
from .serializer import CategorySerializer
from .models import User
from .models import Rol
from .models import Category

# Create your views here.
# Crea todo el CRUD
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class CategoryView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

class RolView(viewsets.ModelViewSet):
    serializer_class = RolSerializer
    queryset = Rol.objects.all()

