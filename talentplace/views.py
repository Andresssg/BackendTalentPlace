from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserSerializer
from .serializer import RolSerializer
from .serializer import CategorySerializer
from .serializer import ServiceSerializer
from .serializer import OfferedServiceSerializer
from .serializer import HiredServiceSerializer
from .models import User
from .models import Rol
from .models import Category
from .models import Service
from .models import OfferedService
from .models import HiredService

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

class ServiceView(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()

class OfferedServiceView(viewsets.ModelViewSet):
    serializer_class = OfferedServiceSerializer
    queryset = OfferedService.objects.all()

class HiredServiceView(viewsets.ModelViewSet):
    serializer_class = HiredServiceSerializer
    queryset = HiredService.objects.all()

