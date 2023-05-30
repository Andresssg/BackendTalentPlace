from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from talentplace import views
from .views import user_register

router = routers.DefaultRouter()
router.register(r"roles", views.RolView, 'roles')
router.register(r"users", views.UserView, 'users')
router.register(r"categories", views.CategoryView, 'categories')
router.register(r"services", views.ServiceView, 'services')
router.register(r"offeredservices", views.OfferedServiceView, 'offeredservices')
router.register(r"hiredservices", views.HiredServiceView, 'hiredservices')

BASE_DIR = "api/v1/"

urlpatterns = [
    #path("ruta",funcion a ejecutar, )
    path(f"{BASE_DIR}", include(router.urls)),
    path(f"{BASE_DIR}register", user_register, name='register'),
    path("docs/", include_docs_urls(title="Talentplace API"))
]