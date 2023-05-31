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

from .serializer import HiredServiceSerializer
from rest_framework import views, status
from .models import User
from .models import Rol
from .models import Category
from .models import Service
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
    searchUser = User.objects.filter(email = request.data.get('offerer_id'))
    firstUser = searchUser.first()
    offererId = firstUser.id_user

    searchCategory = Category.objects.filter(category_name = request.data.get('category_id'))
    firstCategory = searchCategory.first()
    categoryId = firstCategory.id_category

    data_request= request.data.copy()
    data_request['offerer_id'] = offererId
    data_request['category_id'] = categoryId

    serializer = ServiceSerializer(data=data_request)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def modify_service(request):
    

@api_view(['PUT'])
def change_password(request):
    new_password = request.data.get('newpassword')
    email = request.data.get('email')

    if not email or not new_password:
        return Response({'message': 'Los campos estan incompletos'}, status=400)

    search_user = User.objects.filter(email=email)
    first_user = search_user.first()
    if first_user:
        serializer = UserSerializer(first_user, data={'password': make_password(new_password)}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    return Response({'error': 'Usuario no encontrado'}, status=404)
