# Vistas y plantillas

## Introducción

Seguro que has oído hablar del patrón de diseño **Modelo - Vista - Controlador** el cual separa la entidad o **modelo** que se almacena en base de datos en una capa, la **vista** que es la representación en pantalla de los datos y el **controlador** que comunica estas dos partes e incorpora la lógica.

**Django** implementa este patrón, pero lo llama **Model - Template - View**. Es prácticamente lo mismo, pero no confundir **view** con **vista** del modelo descrito anteriormente. En **Django**, **view** equivale al **controlador**.


## Vistas

Una **vista** en **Django** es, simplemente, una **función** que recibe una petición HTTP y genera una respuesta:

```python
from django.http import HttpResponse

def helloworld(request):
    return HttpResponse("helloworld")
```

Para que funcione como una **vista**, habría que incluirlo en el fichero de **urls.py** de la siguiente forma:

```python
from django.urls import path
from miaplicacion.views import helloworld


urlpatterns = [
    path('helloworld/', helloworld, name="helloworld"),
]

```

Entonces, accediendo a `http://127.0.0.1:8000/helloworld` recibiríamos el texto "helloworld".

Tal y como está, la **función** admitiría peticiones de cualquier **método HTTP**. Eso se puede restringir con el **decorador** `require_http_method`:

```python
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def helloworld(request):
    return HttpResponse("helloworld")

```

Y además, podemos indicar que solo puedan acceder usuarios autenticados con `login_required`:

```python
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
@login_required
def helloworld(request):
    return HttpResponse("helloworld")

```
Ahora vamos a implementar una vista de listado y otra de detalle de comentarios:

```python
import os
from django.http import Http404
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from news.models import Comentario


@require_http_methods(["GET"])
def listado_comentarios(request):
    context = {
        "object_list": Comentario.objects.all()
    }
    
    return render(request, os.path.join("news", "comentario_list.html"), context=context)

@require_http_methods(["GET"])
def detalle_comentario(request, pk):
    try:
        context = {
            "object": Comentario.objects.get(pk=pk)
        }
    except Comentario.DoesNotExist:
        raise Http404("No existe el comentario")
    
    return render(request, os.path.join("news", "comentario_detail.html"), context=context)
```

Y se agregaría a urls así:

```python
from django.urls import path
from noticias import views as noticias_views


urlpatterns = [
    path('comentarios/', noticias_views.listado_comentarios, name="listado-comentario"),
    path('comentarios/<int:pk>/', noticias_views.detalle_comentario, name="detalle-comentario"),
]
```


Consiste en dos funciones que reciben como parámetro la petición, la cual se la pasamos a las plantillas junto con el resultado de un **queryset**. Facil, ¿verdad? ¡Pues aún hay una forma más sencilla de trabajar! Con las `GenericView` de **Django**:

```python
from django.views.generic import ListView, DetailView
from news.models import Comentario


class ComentarioDetailView(DetailView):
    model = Comentario


class ComentarioListView(ListView):
    model = Comentario
```

Y se agregarían a `urls` así:

```python
from django.urls import path
from noticias import views as noticias_views


urlpatterns = [
    path('comentarios/', noticias_views.ComentarioListView.as_view(), name="listado-comentario"),
    path('comentarios/<int:pk>/', noticias_views.ComentarioDetailView.as_view(), name="detalle-comentario"),
]
```

Solo con esas pocas lineas, **Django** ha generado dos **views**, una de listado y otra de detalle. Además, a la de detalle le hemos indicado con `<int:pk>` que el detalle lo tiene que obtener usando la **pk** del modelo y que ahí espera un número entero.

El "problema" de esto es que va a intentar renderizar automáticamente las **plantillas** `comentario_list.html` y `comentario_detail.html` pero aún no sabemos que son las **plantillas**...

## Plantillas

Una **plantilla** es un archivo que contiene porciones de código HTML que se rellenará con información que devolvamos en programación.

Por defecto, `Django` va a ir a buscar **plantillas** a las carpetas de cada **aplicación**. Concretamente a "<nombre_aplicacion>/templates/<nombre_aplicacion>". Hago hincapié en que la ruta contiene el nombre de la aplicación dentro de la carpeta templates, porque es fácil que se olvide. Si es necesario, se pueden indicar carpetas manualmente modificando en `settings.py` la variable `TEMPLATES`. Para este ejemplo, he añadido la carpeta `templates` de al raíz del proyecto para incluir ahí la plantilla base, como veremos a continuación:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "upsa_news" / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Las plantillas contienen código HTML, pero con **hooks** donde inyectaremos los objetos en la **view**. Lo ideal es tener un archivo `base.html`
con el esqueleto básico (header, footer, menús, etc) y **bloques** sobreescribibles desde otras plantillas:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <title>Noticias UPSA - {% block title %}Home{% endblock %}</title>
</head>

<body>
    <div id="sidebar">
        {% block menu %}
        <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/noticias/">Noticias</a></li>
            <li><a href="/comentarios/">Comentarios</a></li>
        </ul>
        {% endblock %}
    </div>

    <div id="content">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

En el ejemplo se ve un esqueleto muy básico de **html** con tres secciones **block**: `title`, `menu` y `content`. Contienen valores por defecto, pero se sobreescribirán cuando usemos esos bloques en una plantilla.

Vamos a implementar los ejemplos anteriores para `comentarios`:

- comentario_detail.html:

```html
{% extends "base.html" %}

{% block title %}{{ object.titulo }}{% endblock %}

{% block content %}
<div>{{ object.fecha_publicacion|date }} - {{ object.user.username }}</div>
{% endblock %}
```

- comentario_list.html:
```html
{% extends "base.html" %}

{% block title %}Listado de comentarios{% endblock %}

{% block content %}
    <ul>
        {% for comentario in object_list %}
            <li><a href="/comentarios/{{comentario.pk}}">{{ comentario.fecha_publicacion|date }} - {{ comentario.user.username }}</li></a>
        {% empty %}
            <li>Aún no hay comentarios.</li>
        {% endfor %}
    </ul>
{% endblock %}
```

Como se ve, nunca se sobreescribe el **bloque** menu, y se añade siempre un **bloque** `title` y otro `content`.

## Ejecicios

1. Emula el trabajo hecho para `comentarios` y añade la vista de listado y detalle para `noticias`.