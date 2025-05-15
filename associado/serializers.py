from rest_framework import serializers
from associado.models import Associado, Setor


class AssociadoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Associado
        fields = '__all__'

class SetorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Setor
        fields = '__all__'

