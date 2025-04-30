from rest_framework import generics
from decano.models import Decano
from decano.serializers import DecanoSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class DecanoCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Decano.objects.all()
    serializer_class = DecanoSerializer


class DecanoRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Decano.objects.all()
    serializer_class = DecanoSerializer
