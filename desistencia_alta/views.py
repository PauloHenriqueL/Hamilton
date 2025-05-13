from rest_framework import generics
from fistkiss.models import Desistencia_alta
from fistkiss.serializers import Desistencia_altaSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class Desistencia_altaCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Desistencia_alta.objects.all()
    serializer_class = Desistencia_altaSerializer


class Desistencia_altaRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Desistencia_alta.objects.all()
    serializer_class = Desistencia_altaSerializer
