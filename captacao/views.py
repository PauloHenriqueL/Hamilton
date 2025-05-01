from rest_framework import generics
from captacao.models import Captacao
from captacao.serializers import CaptacaoSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class CaptacaoCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Captacao.objects.all()
    serializer_class = CaptacaoSerializer


class CaptacaoRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Captacao.objects.all()
    serializer_class = CaptacaoSerializer
