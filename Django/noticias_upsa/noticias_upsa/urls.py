"""noticias_upsa URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from noticias import views as noticias_views
from noticias import api_views as noticias_api_views
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("rest_framework.urls", namespace="rest_framework")),
    path('api/comentarios/', noticias_api_views.ComentariosViewSet.as_view()), 
    path('api/comentarios/<int:pk>', noticias_api_views.ComentarioViewSet.as_view()),
    path('comentarios/', noticias_views.ComentarioListView.as_view(), name="listado-comentario"),
    path('comentarios/<int:pk>/', noticias_views.ComentarioDetailView.as_view(), name="detalle-comentario"),
]
