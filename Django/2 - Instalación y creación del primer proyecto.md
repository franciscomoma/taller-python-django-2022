# Instalación y creación del primer proyecto

## Introducción

En este breve capítulo se aborda la instalación del framework y la creación del primer proyecto a través de la línea de comandos.

## Instalación del framework

Como ya se ha visto en el curso, la instalación de **Django** se hace a través del gestor de paquetes **pip**, dado que **Django** está disponible en [**PyPI**](https://pypi.org/project/Django/ "Django en PyPI").

Asegúrate que está activo un **entorno virtual** antes de instalar **Django** o se instalará junto con la instalación global de **Python** del sistema operativo.

Con `pip -V` se puede ver la ruta del entorno activo. Si coincide con la ruta donde tienes tu entorno virtual para el proyecto, continúa con:

```
pip install django==3.1.7
```

Y no olvides añadir `django==3.1.7` al archivo de requisitos (requirements.txt) de tu proyecto. En un equipo de desarrollo lo necesitarás para que el resto de miembros trabajen sobre las mismas versiones.

## Creando el primer proyecto

Una vez instalado **Django** en el entorno virtual, este provee de una **interfaz de línea de comandos (cli)**: `django-admin`.

Además de otras muchas utilidades que estarán disponibles una vez esté creado el proyecto, destaca el comando `startproject`.

Para crear el primer proyecto, basta con ejecutar `django-admin startproject <nombre_del_proyecto>` (usa un nombre válido de variable de **Python**). Esto creará el esqueleto de un proyecto con la siguiente estructura:

- <nombre_del_proyecto> - Raíz del proyecto
    - <nombre_del_proyecto> - Carpeta de la Aplicación Principal
        - \_\_init\_\_.py - Inicializa el módulo <nombre_del_proyecto>
        - asgi.py - Archivo con la configuración del proyecto para **servidores web asíncronos**.
        - settings.py - Archivo con la configuración del proyecto. Se usa a menudo.
        - urls.py - Archivo principal con las **urls** activas en el proyecto.
        - wsgi.py - Archivo con la configuración del proyecto para **servidores web síncronos**.
    - manage.py - Es equivalente a `django-admin`. Permite gestionar diferentes aspectos del proyecto.

Bien, una vez creado, ya se puede arrancar el servidor de desarrollo.

## El servidor de desarrollo

**Django** provee al desarrollador de un **servidor web** de pruebas que será la herramienta principal para el desarrollo con el framework.

Para lanzarlo, ejecuta `python manage.py runserver` y observa la salida:

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

Lo indica que el servidor está escuchando por el puerto 8000 de tu equipo.

La principal característica de este servidor es que se recargará automáticamente cada vez que un archivo `*.py` contenido en la carpeta del proyecto se vea modificado, pero **no es apto para producción** ya que no es un servidor seguro y además, esta característica del recargado lo hace extremadamente lento.

Lo común para desplegar proyectos **Django** es utilizar servidores como [uWSGI](https://uwsgi-docs.readthedocs.io/en/latest/ "uWSGI") o [Gunicorn](https://gunicorn.org/ "Gunicorn"). Más información [aquí](https://docs.djangoproject.com/es/3.1/howto/deployment/ "Desplegando Django").



## Ejercicios

1. Crea un proyecto llamado noticias_upsa.
2. Lanza el servidor de desarrollo y accede, a través de tu navegador, a http://127.0.0.1:8000.
