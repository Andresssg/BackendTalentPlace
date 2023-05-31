from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r"roles", RolView, 'roles')
router.register(r"users", UserView, 'users')
router.register(r"categories", CategoryView, 'categories')
router.register(r"services", ServiceView, 'services')
router.register(r"hiredservices", HiredServiceView, 'hiredservices')

BASE_DIR = "api/v1/"

urlpatterns = [
    #path("ruta",funcion a ejecutar, )
    path(f"{BASE_DIR}", include(router.urls)),
    path(f"{BASE_DIR}register", user_register, name='register'),
    path(f"{BASE_DIR}login", user_login, name='login'),
    path(f"{BASE_DIR}createservice", create_service, name='createservice'),
    path(f"{BASE_DIR}hireservice", hire_service, name='hireservice'),
    path(f"{BASE_DIR}users/chagepassword", change_password, name='changepassword'),
    path("docs/", include_docs_urls(title="Talentplace API"))
]