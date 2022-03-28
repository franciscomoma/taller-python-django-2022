from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from noticias.models import Comentario
from noticias.serializers import ComentarioSerializer



class ComentariosViewSet(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer

    def perform_create(self, serializer):
        # Así podemos asignar el comentario al usuario logeado fácilmente
        serializer.is_valid()

        instance = Comentario(autor=self.request.user, **serializer.validated_data)
        instance.save()

class ComentarioViewSet(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly,]
    queryset = Comentario.objects.all()
    serializer_class = ComentarioSerializer
