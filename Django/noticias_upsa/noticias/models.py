from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()

# Create your models here.

#from scrapper import obtener_noticias
#from datetime import datetime
import hashlib
import json


RUTA_AL_ARCHIVO = 'noticias.json'


class Noticia(models.Model):
    titulo = models.CharField(max_length=250)
    resumen = models.CharField(max_length=500)
    categoria = models.CharField(max_length=15)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    enlace = models.CharField(max_length=250)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)

    #def __init__(self, titulo, resumen, categoria, autor, enlace, fecha_publicacion):
    #    self.titulo = titulo
    #    self.resumen = resumen
    #    self.categoria = categoria
    #    self.autor = autor
    #    self.enlace = enlace
    #    self.fecha_publicacion = fecha_publicacion

    def __str__(self):
        return f"{self.fecha_publicacion.strftime('%Y-%m-%d %H:%M')} - {self.titulo} - {self.autor}"


    #def as_dict(self):
    #    return {
    #        "titulo": self.titulo,
    #        "resumen": self.resumen,
    #        "categoria": self.categoria,
    #        "autor": self.autor,
    #        "enlace": self.enlace,
    #        "fecha_publicacion": self.fecha_publicacion.strftime('%Y-%m-%d %H:%M')
    #    }

    @property
    def hash(self):
        id = hashlib.md5(f"{self.titulo}{self.autor}".encode()).hexdigest()
        return id

    """
    @classmethod
    def recover(cls, id):
        noticias = {}

        with open(RUTA_AL_ARCHIVO, 'r') as archivo:
            contenido = ''.join(archivo.readlines())
            if contenido:
                noticias = json.loads(contenido)
        
        if id in noticias:
             obj_noticia = noticias.get(id)
             obj_noticia['fecha_publicacion'] = datetime.strptime(obj_noticia.get('fecha_publicacion'), '%Y-%m-%d %H:%M')

             return cls(**noticias.get(id))
    """

class Comentario(models.Model):
    texto = models.CharField(max_length=200, help_text="Añade aquí el texto de tu comentario", verbose_name="Texto del comentario")
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    noticia = models.ForeignKey(Noticia, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return f"{self.fecha_publicacion.strftime('%Y-%m-%d %H:%M')} - {self.autor}"
