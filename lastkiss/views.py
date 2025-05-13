from rest_framework import generics
from fistkiss.models import Lastkiss
from fistkiss.serializers import LastkissSerializer
from rest_framework.permissions import IsAuthenticated
from app.permissions import GlobalDefaultPermission


class LastkissCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Lastkiss.objects.all()
    serializer_class = LastkissSerializer


class LastkissRetrieveUpdateDestoyView(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalDefaultPermission,)
    queryset = Lastkiss.objects.all()
    serializer_class = LastkissSerializer
