from rest_framework import generics
from registro.models import Registro
from registro.serializers import RegistroSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class RegistroCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer


class RegistroRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer
