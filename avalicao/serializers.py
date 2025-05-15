from rest_framework import serializers
from avalicao.models import Avaliacao, Avaliado, Avaliador


class AvaliacaoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliacao
        fields = '__all__'

class AvaliadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliado
        fields = '__all__'

class AvaliadorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Avaliador
        fields = '__all__'
