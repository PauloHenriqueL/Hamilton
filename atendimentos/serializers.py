from rest_framework import serializers
from atendimentos.models import Atendimento


class AtendimentoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Atendimento
        fields = '__all__'
