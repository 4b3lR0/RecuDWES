"""
URL configuration for RecuDWES project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.template.defaultfilters import title
from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import permission_classes
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from Recu import views
from Recu.views import Show_Recipes, Register, del_Boss

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentación",
        default_version="v1",
        description="Documentación de la API",
    ),
    public=True,
    permission_classes=[AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-token-auth/', ObtainAuthToken.as_view(), name='login'),
    path('register/', Register.as_view(), name='Register'),
    path('delBoss/<int:id>', del_Boss.as_view(), name='Borrar Jefe'),
    path('showRecipes/<str:m_name>/<int:page>', Show_Recipes.as_view(), name='Mostrar Recetas'),

    path('createBoss/', views.New_Boss),

    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema_swagger_ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema_redoc'),
]