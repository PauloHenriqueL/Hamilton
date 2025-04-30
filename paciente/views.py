from rest_framework import generics
from paciente.models import Paciente
from paciente.serializers import PacienteSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class PacienteCreateViewList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer


class PacienteRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Paciente.objects.all()
    serializer_class = PacienteSerializer
