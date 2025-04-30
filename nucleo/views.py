from rest_framework import generics
from nucleo.models import Nucleo
from nucleo.serializers import NucleoSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class NucleoCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer


class NucleoRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Nucleo.objects.all()
    serializer_class = NucleoSerializer
