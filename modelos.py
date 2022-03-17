from scrapper import obtener_noticias
from datetime import datetime
import hashlib
import json


RUTA_AL_ARCHIVO = 'noticias.json'


class Noticia:
    titulo = ""
    resumen = ""
    categoria = ""
    autor = ""
    enlace = ""
    fecha_publicacion = None

    def __init__(self, titulo, resumen, categoria, autor, enlace, fecha_publicacion):
        self.titulo = titulo
        self.resumen = resumen
        self.categoria = categoria
        self.autor = autor
        self.enlace = enlace
        self.fecha_publicacion = fecha_publicacion

    def __str__(self):
        return f"{self.fecha_publicacion.strftime('%Y-%m-%d %H:%M')} - {self.titulo} - {self.autor}"

    def as_dict(self):
        return {
            "titulo": self.titulo,
            "resumen": self.resumen,
            "categoria": self.categoria,
            "autor": self.autor,
            "enlace": self.enlace,
            "fecha_publicacion": self.fecha_publicacion.strftime('%Y-%m-%d %H:%M')
        }

    @property
    def id(self):
        id = hashlib.md5(f"{self.titulo}{self.autor}".encode()).hexdigest()
        return id

    def save(self):
        noticias = {}

        try:
            with open(RUTA_AL_ARCHIVO, 'r') as archivo:
                contenido = ''.join(archivo.readlines())
                if contenido:
                    noticias = json.loads(contenido)
        except FileNotFoundError:
            pass

        noticias[self.id] = self.as_dict()

        with open(RUTA_AL_ARCHIVO, 'w') as archivo:
             archivo.write(json.dumps(noticias, indent=4))


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


noticias, peticiones_hechas = obtener_noticias()

for noticia in noticias:
    obj_noticia = Noticia(**noticia)
    obj_noticia.save()

