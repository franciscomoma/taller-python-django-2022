from django.views.generic import ListView, DetailView
from noticias.models import Comentario


class ComentarioDetailView(DetailView):
    model = Comentario


class ComentarioListView(ListView):
    model = Comentario
