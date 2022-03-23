# Consultas a la base de datos

## Introducción

Como ya mencionamos antes, **Django** utiliza **bases de datos relacionales** (SQL) para almacenar datos de sus **modelos**, pero esta tarea está simplificada a través de un potente **ORM** (Object Relational Mapping) que además optimiza al máximo las consultas.

## El ORM de Django

Cualquier clase que hereda de `Model` hemos visto que es capaz de generar **migraciones**, es decir, lleva su estructura a **tablas** de una base de datos relacional.

Pero, además de esto, incorpora la funcionalidad de consultas. Por ejemplo:

```python
from noticias.models import Comentario

Comentario.objects.all()    
```

Este simple método, devuelve un **iterador** llamado **queryset** que contiene todos los registros de la tabla de la base de datos. Pero es más, hasta que no se accdede a ellos, no ejecuta ninguna consulta.

Esa consulta anterior equivaldría a un `select * from noticias_comentario`.

¿Podemos filtrar los resultados? Pues claro, con `.filter()` podemos filtrar resultados que cumplan unos parámetros concretos. Por ejemplo:

```python
from noticias.models import Comentario
from datetime import datetime, timezone


Comentario.objects.filter(fecha_publicacion__gt=datetime(2020, 1, 1, tzinfo=timezone.utc), fecha_publicacion__lt=datetime(2020, 2, 1, tzinfo=timezone.utc))
```

Con eso se obtendrían los `comentarios` comprendidos entre el 1 de enero y el 1 de febrero de 2020 y equivaldría a `select * from noticias_comentario where fecha_publicacion between '2020-01-01' and '2020-02-01'`.

También se pueden hacer inserciones creando un nuevo objeto, añadiendo su información y llamando a `.save()`:

```python
from noticias.models import Comentario
from datetime import datetime, timezone
from django.contrib.auth import get_user_model

User = get_user_model()

yo = User.objects.get(username="fmolina")

nuevo_comentario = Comentario()
nuevo_comentario.autor = yo
nuevo_comentario.texto = "Este es mi nuevo comentario"
nuevo_comentario.save()

print(nuevo_comentario.pk)
```

He aprovechado también para introducir `.get()`. Actúa como `.filter()`, pero en lugar de devolver un **queryset** devuelve un objeto. Si no existe el criterio de búsqueda, lanzará una excepción.

Puedes profundizar más sobre **querysets** en [este enlace](https://docs.djangoproject.com/en/3.1/topics/db/queries/ "Django - Querysets").


## Ejercicios

1. Ejecuta una shell de Django con `python manage.py shell`. Esto es una consola interactiva que usaremos como un **Jupyter**.
2. Una vez ahí, importa los modelos de la **aplicación** `noticias`.
3. Realiza consultas sobre las `noticias` que creamos en el apartado anterior.