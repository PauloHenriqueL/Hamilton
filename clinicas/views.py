from rest_framework import generics
from clinicas.models import Clinica
from clinicas.serializers import ClinicaSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class ClinicaCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer


class ClinicaRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Clinica.objects.all()
    serializer_class = ClinicaSerializer
