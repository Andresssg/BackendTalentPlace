from datetime import date
from functools import wraps
import base64

import smtplib
from email.mime.text import MIMEText

from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import TokenError, AccessToken

from django.http import HttpResponseBadRequest
from django.core.files.images import ImageFile


from .serializer import UserSerializer
from .serializer import RolSerializer
from .serializer import CategorySerializer
from .serializer import ServiceSerializer
from .serializer import TokenSerializer
from .serializer import HiredServiceSerializer

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

def send_email(subject, body, email):
    sender = "talentplac3@gmail.com"
    recipients = [f'{email}']
    password = "pcexjppuyawsxuvr"

    image_url = 'https://static.wixstatic.com/media/9b1600_dcc519d299a448debea913eef5d31775~mv2.png/v1/fill/w_129,h_84,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/logo2.png'
    message = f"""\
    <html>
    <head>
        <title>{subject}</title>
    </head>
    <body>
        <table width="100%" cellpadding="0" cellspacing="0">
            <tr>
                <td align="center" bgcolor="#f2f2f2" style="padding: 40px 0;">
                    <img src="{image_url}" alt="Logo de la Empresa" width="200">
                    <h2>{subject}</h2>
                    <p>{body}</p>
                    <p>Si tienes alguna pregunta o necesitas ayuda, no dudes en contactarnos.</p>
                    <p>Atentamente,</p>
                    <p>El equipo de <span style="color: red;">Talent Place</span></p>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)

    try:
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()
        print("El correo electrónico se envió correctamente.")
    except Exception as e:
        print("Error al enviar el correo electrónico:", str(e))


def check_auth():
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            tokenSent = request.META.get('HTTP_TOKEN')
            if tokenSent is None:
                return Response({'message': 'Inicie sesión.'}, status=401)

            try:
                access_token = AccessToken(tokenSent)
                access_token.verify()
            except TokenError:
                return Response({'message': 'Token inválido o expirado.'}, status=401)
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def role_required(rol_id):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            tokenSent = request.META.get('HTTP_TOKEN')
            access_token = AccessToken(tokenSent)
            rol = access_token.get('rol')
            if rol not in rol_id:
                return Response({'message': 'Usuario no autorizado.'}, status=401)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

@api_view(['POST'])
def user_register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        data['password'] = make_password(data['password'])
        serializer.save()
        send_email("Registro exitoso en la plataforma", "Bienvenido a Talentplace", data['email'])
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def user_login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(request, email=email, password=password)

    if user is None:
        return Response({'message': 'Usuario y/o contraseña incorrecta.'}, status=status.HTTP_401_UNAUTHORIZED)
    
    tokenSerializer = TokenSerializer()
    claim_token = tokenSerializer.get_token(user)
    token = str(claim_token.access_token)
    resUser = UserSerializer(user)
    return Response({"token": token, "user": resUser.data},status=200)

@api_view(['GET'])
def get_all_services(request):
    services = Service.objects.filter(available=True)
    serializer = ServiceSerializer(services, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@check_auth()
@role_required([3])
def get_all_users(request):
    users = User.objects
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@check_auth()
@role_required([2, 3])
def hire_service(request):
    email = request.data.get("email")
    idService = request.data.get("service_id")
    if not email or not idService:
        return Response({'message': 'Los campos están incompletos'})
    searchUser = User.objects.filter(email = f'{email}')
    firstUser = searchUser.first()
    applicantId = firstUser.id_user
    serviceDate = date.today()

    data_request = request.data.copy()
    data_request['applicant_id'] = applicantId
    data_request['request_date'] = serviceDate

    serializer = HiredServiceSerializer(data=data_request)
    if serializer.is_valid():
        serializer.save()
        send_email("Contrato de servicio exitoso", "Has contratado un servicio", email)
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
@check_auth()
@role_required([1, 3])
def create_service(request):
    searchUser = User.objects.filter(email = request.data.get('email'))
    firstUser = searchUser.first()
    offererId = firstUser.id_user

    searchCategory = Category.objects.filter(category_name = request.data.get('category'))
    firstCategory = searchCategory.first()
    categoryId = firstCategory.id_category

    data_request= request.data.copy()

    if 'evidence_img' in request.data:
        try:
            img = request.FILES['evidence_img']
            image_type = img.content_type
            imagen_binaria = img.read()
            imagen_base64_data = base64.b64encode(imagen_binaria).decode('utf-8')
            imagen_base64 = f"data:{image_type};base64,{imagen_base64_data}"
            data_request['evidence_img'] = imagen_base64
        except IOError:
            return HttpResponseBadRequest('No se pudo abrir la imagen.')

    data_request['offerer_id'] = offererId
    data_request['category_id'] = categoryId
    data_request['available'] = True

    serializer = ServiceSerializer(data=data_request)
    if serializer.is_valid():
        serializer.save()
        send_email("Creación de servicio exitosa", "Has creado tu nuevo servicio, esperamos que sea muy apoyado", firstUser.email)
        return Response({"message": "Servicio creado exitosamente."}, status=201)
    return Response({"message": "No se ha podido crear el servicio", "errors": serializer.errors}, status=400)

@api_view(['GET'])
@check_auth()
@role_required([1, 3])
def get_services_by_user(request):
    username = request.GET.get('username')
    if not username:
        return Response({"message": "No se proporcionaron parámetros de consulta"}, status=400)
    searchUser = User.objects.filter(username=username)
    firstUser = searchUser.first()
    if(firstUser is None):
        return Response({"message": "No se encontró el usuario"}, status=404)
    idUser = firstUser.id_user
    searchServices = Service.objects.filter(offerer_id=idUser).filter(available=True)
    serializer = ServiceSerializer(searchServices, many=True)
    return Response({'services': serializer.data}, status=200)
    
@api_view(['GET'])
@check_auth()
@role_required([2, 3])
def get_hired_by_user(request):

    username = request.GET.get('username')

    if not username:
        return Response({"message": "No se proporcionaron parámetros de consulta"}, status=400)
    
    searchUser = User.objects.filter(username=username)
    firstUser = searchUser.first()

    if(firstUser is None):
        return Response({"message": "No se encontró el usuario"}, status=404)
    
    idUser = firstUser.id_user
    searchHiredServices = HiredService.objects.filter(applicant_id=idUser)
    serializer = HiredServiceSerializer(searchHiredServices, many=True)

    for item in serializer.data:
        service_id = item["service_id"]
        service = Service.objects.get(id_service=service_id)
        offerer = service.offerer_id
        item["full_name"] = f"{offerer.name} {offerer.lastname}"
        serviceSerializer = ServiceSerializer(service)
        item["service"]= serviceSerializer.data

    return Response({'services': serializer.data}, status=200)

@api_view(['PUT'])
@check_auth()
@role_required([1, 3])
def modify_service(request):
    servicio = Service.objects.get(id_service=request.data.get('id_service'))
    data_request= request.data.copy()
    
    tokenSent = request.META.get('HTTP_TOKEN')
    access_token = AccessToken(tokenSent)
    rol_client = access_token.get('rol')
    id_user_client = access_token.get('id_user')

    offerer_id = servicio.offerer_id.id_user

    if id_user_client != offerer_id and rol_client != 3:
        return Response({'message': 'No tienes ningún servicio con ese id'}, status=404)

    if 'category' in request.data:
        searchCategory = Category.objects.filter(category_name = request.data.get('category'))
        firstCategory = searchCategory.first()
        categoryId = firstCategory.id_category
        data_request['category_id'] = categoryId

    if 'evidence_img' in request.data:
        try:
            img = request.FILES['evidence_img']
            image_type = img.content_type
            imagen_binaria = img.read()
            imagen_base64_data = base64.b64encode(imagen_binaria).decode('utf-8')
            imagen_base64 = f"data:{image_type};base64,{imagen_base64_data}"
            data_request['evidence_img'] = imagen_base64
        except IOError:
            return HttpResponseBadRequest('No se pudo abrir la imagen.')

    serializer = ServiceSerializer(servicio, data=data_request, partial=True)

    if serializer.is_valid():
        data = serializer.validated_data
        for field, value in data.items():
            setattr(servicio, field, value)
        servicio.save()
        send_email("Modificación exitosa de servicio", "Has modificado un servicio", access_token.get('email'))
        return Response({"message": "Servicio modificado exitosamente."}, status=201)
    return Response({"message": "No se ha podido modificar el servicio", "errors": serializer.errors}, status=400)

@api_view(['PUT'])
@check_auth()
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
            send_email("Cambio de contraseña exitoso", "Has cambiado tu contraseña, si no fuiste tú contactate con soporte.", email)
            return Response({'message': 'Contraseña cambiada exitosamente'}, status=200)
        return Response({'message': 'Problema al cambiar la contraseña', 'errors': serializer.errors}, status=400)
    return Response({'message': 'Usuario no encontrado'}, status=404)

@api_view(['DELETE'])
@check_auth()
@role_required([1, 3])
def delete_service(request):
    servicio = Service.objects.get(id_service=request.data.get('id_service'))
    serviceId = request.data.get('id_service')

    tokenSent = request.META.get('HTTP_TOKEN')
    access_token = AccessToken(tokenSent)
    rol_client = access_token.get('rol')
    id_user_client = access_token.get('id_user')

    offerer_id = servicio.offerer_id.id_user

    if id_user_client != offerer_id and rol_client != 3:
        return Response({'message': 'No tienes ningún servicio con ese id'}, status=404)

    search_service = Service.objects.filter(id_service=serviceId)
    first_service = search_service.first()
    if first_service:
        serializer = ServiceSerializer(first_service, data={'available': False}, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_email("Eliminación exitosa del servicio", "Has eliminado un servicio.", access_token.get('email'))
            return Response({'message': 'Servicio eliminado exitosamente'}, status=200)
        return Response({'message': 'Problema al eliminar el servicio', 'errors': serializer.errors}, status=400)
    return Response({'error': 'Servicio no encontrado'}, status=404)
