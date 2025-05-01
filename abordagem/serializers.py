from rest_framework import serializers
from abordagem.models import Abordagem


class AbordagemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Abordagem
        fields = '__all__'
