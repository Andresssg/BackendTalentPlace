from datetime import date
from django.shortcuts import render
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import UserSerializer
from .serializer import RolSerializer
from .serializer import CategorySerializer
from .serializer import ServiceSerializer
from .serializer import OfferedServiceSerializer
from .serializer import HiredServiceSerializer
from rest_framework import views, status
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

@api_view(['POST'])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data['password'] = make_password(data['password'])
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)
    if user is not None:
        return Response({'message': 'Usuario autenticado correctamente.'})
    else:
        return Response({'message': 'Usuario y/o contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def hire_service(request):
    email = request.data.get("email")
    offeredServiceId = request.data.get("offeredservice")
    price = request.data.get("price")
    if email is None or offeredServiceId is None or price is None:
        return Response({'message': 'Los campos están incompletos'})
    searchUser = User.objects.filter(email = f'{email}')
    firstUser = searchUser.first()
    applicantId = firstUser.id_user
    serviceDate = date.today()

    return Response({'message': 'hola hire',
                     'applicantid': applicantId, 'offeredservicedid': offeredServiceId,
                     'price': price, 'date': serviceDate})

@api_view(['POST'])
def create_service(request):
    serializer = ServiceSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)