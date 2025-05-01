from rest_framework import serializers
from captacao.models import Captacao


class CaptacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Captacao
        fields = '__all__'
