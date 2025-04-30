from rest_framework import generics
from terapeuta.models import Terapeuta
from terapeuta.serializers import TerapeutaSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission

class TerapeutaCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Terapeuta.objects.all()
    serializer_class = TerapeutaSerializer


class TerapeutaRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Terapeuta.objects.all()
    serializer_class = TerapeutaSerializer
