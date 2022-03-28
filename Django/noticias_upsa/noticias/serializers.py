from rest_framework import serializers
from noticias.models import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    autor = serializers.SlugRelatedField(slug_field="username", read_only=True)

    class Meta:
        fields = ("id", "texto", "fecha_publicacion", "autor")
        model = Comentario
