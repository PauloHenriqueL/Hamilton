from rest_framework import generics
from abordagem.models import Abordagem
from abordagem.serializers import AbordagemSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class AbordagemCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Abordagem.objects.all()
    serializer_class = AbordagemSerializer


class AbordagemRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Abordagem.objects.all()
    serializer_class = AbordagemSerializer
