from rest_framework import generics
from modalidades.models import Modalidade
from modalidades.serializers import ModalidadeSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class ModalidadeCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer


class ModalidadeRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Modalidade.objects.all()
    serializer_class = ModalidadeSerializer
