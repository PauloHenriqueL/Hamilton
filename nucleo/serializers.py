from rest_framework import serializers
from nucleo.models import Nucleo


class NucleoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Nucleo
        fields = '__all__'
