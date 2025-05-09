from rest_framework import generics
from fistkiss.models import Fistkiss
from fistkiss.serializers import FistkissSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class FistkissCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Fistkiss.objects.all()
    serializer_class = FistkissSerializer


class FistkissRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Fistkiss.objects.all()
    serializer_class = FistkissSerializer
