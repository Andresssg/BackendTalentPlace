from django.shortcuts import render
from rest_framework import viewsets
from .serializer import UserSerializer
from .models import User

# Create your views here.
# Crea todo el CRUD
class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

