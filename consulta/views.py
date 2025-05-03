from rest_framework import generics
from consulta.models import Consulta
from consulta.serializers import ConsultaSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class ConsultaCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer


class ConsultaRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Consulta.objects.all()
    serializer_class = ConsultaSerializer
