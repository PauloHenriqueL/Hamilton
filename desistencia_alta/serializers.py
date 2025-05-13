from rest_framework import serializers
from fistkiss.models import Desistencia_alta


class Desistencia_altaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Desistencia_alta
        fields = '__all__'
