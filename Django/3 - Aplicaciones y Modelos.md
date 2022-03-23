# Aplicaciones y Modelos

## Introducción

En **Django** dividiremos el código en **aplicaciones** que ejecutarán un propósito concreto, como por ejemplo, una **aplicación** de blogging que permite crear *posts*, *escribir comentarios*, *dar a like*, etc.

Una aplicación puede tener asociados **modelos** que representan los objetos a almacenar.


## Crear una aplicación de Django

Al igual que cuando se crea un **proyecto**, existe un comando de `django-admin` que realiza esta tarea, pero como en este punto el proyecto ya existe, lo llamaremos con `python manage.py`.

El comando es `startapp <nombre_de_la_aplicación>`.

Crear una nueva aplicación generará la siguiente estructura de directorios en la misma carpeta que se sitúa **manage.py**:

- <nombre_de_la_aplicación> - La carpeta que contiene la aplicación.
    - migrations - Esta carpeta contendrá las **migraciones de los modelos de la aplicación**.
    - admin.py - Este archivo especifica como se comportará el **administrador de Django** con los modelos de esta aplicación.
    - apps.py - Este archivo especifica la información de la propia aplicacion.
    - models.py - Aquí se crearán los **modelos**, es decir, las entidades que forman parte de la **aplicación**.
    - tests.py - Los tests unitarios para la **aplicación**.
    - views.py - Aquí se implementarán las **vistas** de la aplicación.

Como se ve aquí, introducimos un montón de conceptos nuevos como **migraciones**, **administrador de Django** o **vistas**. Cada uno se verá en su sección correspondiente, ¡paciencia!

Lo siguiente que hay que hacer ahora es registrar la aplicación recién creada en la **configuración de Django**, por lo que en `<nombre_del_proyecto>/settings.py` se añadirá a la lista `INSTALLED_APPS` el <nombre_de_la_aplicación> y el nombre de la clase de la aplicación. Viene por defecto en apps.py:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    '<nombre_de_la_aplicación>.apps.<nombre_de_la_aplicación>Config'
]
```

En este punto **Django** ya conoce la existencia de la aplicación que está recién creada. Ahora hay que vestirla con funcionalidad, y para ello hay que añadir las entidades que forman parte de ella. O mejor dicho, los **modelos**.


## Añadiendo modelos a una aplicación

Un **modelo** es una entidad que se puede almacenar. O dicho de otro modo... ¡un **modelo** es una clase!

Pero **Django** está pensado para trabajar con una **base de datos relacional**, por lo que en este caso, los **atributos** de la **clase** sí tienen que especificar su tipo.

Todo esto nos lo provee el módulo `django.db.models`, que como se puede apreciar, ya viene importado por defecto al crear la aplicación en el archivo `models.py`.

Un ejemplo de `modelo` puede ser `Comentario`:

```python

from django.db import models


class Comentario(models.Model):
    texto = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
```

Por no entrar aquí en detalle, los campos admitidos por **Django** son [estos](https://docs.djangoproject.com/en/3.1/ref/models/fields/# "Referencia - Campos de Django").

La intención de crear **modelos**, como vimos antes, es poder representar luego estas **clases** como tablas de una **base de datos**.

Pero en una **base de datos**, las **entidades** se relacionan entre sí:

```python
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Comentario(models.Model):
    texto = models.CharField(max_length=200)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
```

En ese caso, se añade una **relación** 1:1 de `Comentario` a `User` (un comentario solo pertenece a un usuario) y 1:N de `User` a `Comentario` (un usuario puede tener varios comentarios). No profundiaré más en relaciones entre tablas en **Django** pero al menos os hacéis una idea.

¡Una aclaración! Como se puede ver en el ejemplo, no he importado diréctamente el **modelo** `User`. Esto es así porque es posible especificar una clase [**User** en `settings.py`](https://docs.djangoproject.com/en/3.1/ref/settings/#auth-user-model). Os recomiendo encarecidamente leer [esta sección](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#auth-custom-user) ya que si no se hace esto al principio de un proyecto, no se puede hacer más adelante y es tremendamente útil tener la posibilidad de añadir campos nuevos al **modelo** `User`. Luego, allá donde se use, se puede recuperar con `get_user_model`.


## Ejercicios

1. Crea una aplicación llamada `noticias`.
2. Recupera la clase `Noticias` de la parte anterior y conviértela en un **modelo** de **Django**. Date cuenta que ahora hereda de `Model`, por lo que no sirve el constructor anterior.
3. Añade también el modelo `Comentario` del ejemplo.
