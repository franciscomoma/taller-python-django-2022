# Django Rest Framework

## Introducción

**Django Rest Framework** es un **paquete** que se integra sobre **Django** para añadir funcionalidad de **API Rest**.


## Instalación

Al igual que **Django**, se instala sobre el entorno virtual con pip, dado que está [disponible en PyPI](https://pypi.org/project/djangorestframework/ "PyPI - Django Rest Framework"):

```
pip install djangorestframework==3.12.2
```

Y como siempre, añade `djangorestframework==3.12.2` a tu requirements.txt.

Con **Django Rest Framework** ya instalado, lo siguiente será añadir `rest_framework` a la lista `INSTALLED_APPS` en `settings.py` del proyecto `Django`:

```python

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'noticias',
    'cuentas',
    'rest_framework'
]
```

Ya vimos que **Django** incluye una consola de administración. **Django Rest Framework** incluye **vistas** para realizar peticiones al **API Rest**. Para incluir esas **vistas**, hay que añadirlas a **urls**:

```python

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include("rest_framework.urls", namespace="rest_framework")),
]
```

Por último, **Django Rest Framework** tiene su propia sección de configuración en `settings.py`, el diccionario `REST_FRAMEWORK`. [Ver la referencia](https://www.django-rest-framework.org/api-guide/settings/ "Django Rest Framework - Settings") en caso de necesitar utilizar una configuración específica.


## Vistas y serializadores 

Ya sabemos que **Django** trabaja con **vistas** o **views**, pero hasta ahora esas **vistas** se han utilizado para renderizar plantillas html.

El próposito de un **API Rest** no es el de mostrar la información a un usuario, si no exponer y consumir datos entre servicios, por lo que **Django Rest Framework** no utiliza **plantillas**, utiliza **serializadores** que son **clases** que se encargan de convertir **objetos** a un formato serializado y viceversa. Un formato muy común es **JSON** y es el que usa **Django Rest Framework** por defecto.

Como hicimos con las **vistas** de **Django**, vamos a implementar una **vista** sencilla con **Django Rest Framework** con el decorador `@api_view`:

```python
from rest_framework.decorators import api_view

@api_view()
def hello_world(request):
    return Response({"message": "Hello, world!"})
```

Y, ya puestos, vamos a implementar todo el **CRUD** (Create - Retrieve - Update - Delete) de `Comentarios`.

- Lo primero es crear el ``Serializer`` para el modelo de `Comentario`:

```python
from rest_framework import serializers
from news.models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    autor = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "texto", "fecha_publicacion", "user")
        model = Comentario
```

Se pueden hacer `Serializers` personalizados, pero ya que queremos **serializar** un modelo, usamos **ModelSerializer**. Solamente hay que indicar que campos no son exáctamente iguales a los del **modelo** (el usuario lo queremos representar con su nombre de usuario, no con el id como saldría por defecto).

Después, se crea una **clase** `Meta` en la que indicamos el **modelo** y los campos del mismo que se van a representar.

Una vez teniendo el `Serializer`, vamos a implementar las **vistas basadas en funciones** con el decorador `@api_view`:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import serializers, status
from news.models import Comentario


class ComentarioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "texto", "fecha_publicacion", "user")
        model = Comentario


@api_view(["GET", "POST"])
def comentarios(request):

    if request.method == "GET":
        queryset = Comentario.objects.all()
        serializer = ComentarioSerializer(queryset, many=True)
        return Response(serializer.data)

    if request.method == "POST":
        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comentario = Comentario(**serializer.validated_data)
            comentario.user = request.user
            comentario.save()

            response_serializer = ComentarioSerializer(comentario)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def comentario(request, pk):
    try:
        comentario = Comentario.objects.get(pk=pk)
    except Comentario.DoesNotExist:
        return Response({"detail": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data)

    if request.method == "PUT":

        serializer = ComentarioSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comentario.texto = serializer.validated_data["texto"]
            comentario.save()

            response_serializer = ComentarioSerializer(comentario)
            return Response(response_serializer.data, status=status.HTTP_200_OK)

    if request.method == "DELETE":
        comentario.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)
```

Con esto ya solo faltaría añadir estas **vistas** a las **urls**:

```python
from django.urls import path
from noticias import api


urlpatterns = [
    path('api/comentarios/', api.comentarios), 
    path('api/comentarios/<int:pk>', api.comentario),
]
```

¡Pero esto es **Django**! Si trabajamos con **modelos**, aún hay una forma mas inmediata de hacer las cosas, con **vistas basadas en clase**:

```python
from noticias.models import Comentario
from rest_framework import serializers, generics


class ComentarioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "texto", "fecha_publicacion", "user")
        model = Comentario


class Comentarios(generics.ListCreateAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

class Comentario(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

```

¡Y con eso ya está! Evidentemente esto proporciona una funcionalidad básica, pero como **Django** y **Django Rest Framework** están preparados para solucionar la mayoría de los problemas comunes del desarrollo web, este tipo de cosas están previstas.

## Permisos

Se pueden limitar permisos tanto en las **vistas basadas en función** como en las **vistas basadas en clase**. Los permisos ya implementados están en `rest_framework.permissions`, pero se pueden personalizar. Para aplicar las restricciones:

- Vistas basadas en función: Con el decorador`@permission_classes`:

```python
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
@permissions_classes([IsAuthenticated,])
def mi_vista(request):
    Response("helloworld")

```

- Vistas basadas en clase: Con el atributo `permission_classes`:

```python

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


class MyView(generics.APIView):
    permission_classes = [IsAuthenticated,]


```

Cuando se añaden varias **PermissionClasses**, el usuario tendrá permisos cuando todas ellas devuelvan `true`.


## Ejercicios

1. Añade el **CRUD** de `comentario` a tu proyecto.
2. Basándote en él, implementa lo mismo para `noticia`.
