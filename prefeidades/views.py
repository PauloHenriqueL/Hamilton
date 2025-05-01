from rest_framework import generics
from prefeidades.models import Prefeidade
from prefeidades.serializers import PrefeidadeSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class PrefeidadeCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Prefeidade.objects.all()
    serializer_class = PrefeidadeSerializer


class PrefeidadeRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Prefeidade.objects.all()
    serializer_class = PrefeidadeSerializer
