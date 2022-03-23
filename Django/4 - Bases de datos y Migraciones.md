# Bases de datos y Migraciones

## Introducción

Cada vez que se agrega un **modelo** a una **aplicación** registrada de **Django**, este debe reflejarse en una **base de datos** para que **Django** sea capaz de persistir sus datos.

## Configurar una base de datos

Por defecto, **Django** se suministra con una conexión a una **base de datos** **Sqlite**:

```python
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

- Sqlite es una pequeña **base de datos** relacional autocontenida (no necesitas un servidor para ejecutarla) y portable (realmente es un fichero).

Pero **Django** es también compatible **Postgres**, **MySQL** y **Oracle** por defecto y con otros muchos motores de **base de datos** no soportados oficialmente.

En la [documentación oficial](https://docs.djangoproject.com/en/3.1/ref/settings/#databases "Django - Bases de datos") se explica como conectar con otros motores de **base de datos**.


## Migraciones

Una **migración** es la actualización de una tabla en una **base de datos** con los cambios que han sufrido los **modelos** de una **aplicación**.

Es decir, cada vez que necesitemos añadir un campo nuevo aun **modelo**, debemos generar **migraciones** que lo reflejen. En ese caso, además, debemos indicar como actuar con los registros ya existentes en esa tabla. Pero no te preocupes, es un comando incluido en `django-admin`: `makemigrations`. Con `python manage.py makemigrations` se generarán automáticamente las migraciones a aplicar, si existieran.

Las **migraciones** se realizan de forma incremental, es decir, si ya hay **modelos** creados y se hacen modificaciones sobre ellos, crearán una nueva **migración** que añade ese cambio sobre la tabla existente.

De hecho, cuando lanzamos el **servidor de desarrollo de Django** nos avisa si quedan **migraciones** pendientes de aplicar:

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
<datetime>
Django version 3.1.7, using settings '<datetime>.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Y además indica que se aplican con `python manage.py migrate`.


## Ejercicios

1. Ejecuta `makemigrations` para generar las migraciones de las nuevas apps que hemos generado.
2. Una vez generadas, lanza el servidor de desarrollo para observar si nuestras apps están incluidas en el mensaje. Después, cierra el servidor de desarrollo con CTRL+C.
3. Después, aplicalas con `migrate`.
4. Ahora que ya tenemos una **base de datos** operativa y con las migraciones aplicadas, ejecuta `python manage.py --help` y busca la manera de crear un superusuario y crealo.
