from django.contrib import admin
from noticias.models import Comentario, Noticia

# Register your models here.
#admin.site.register(Comentario)

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    #fields = ('texto', 'autor')
    list_display = ('pk', 'texto', 'autor')


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'titulo', 'autor', 'hash')
