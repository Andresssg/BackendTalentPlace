from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from talentplace import views

router = routers.DefaultRouter()
router.register(r"roles", views.RolView, 'roles')
router.register(r"users", views.UserView, 'users')
router.register(r"categories", views.CategoryView, 'categories')

urlpatterns = [
    #path("ruta",funcion a ejecutar, )
    path("api/v1/", include(router.urls)),
    path("docs/", include_docs_urls(title="Talentplace API"))
]