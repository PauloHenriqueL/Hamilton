from rest_framework import serializers
from prefeidades.models import Prefeidade


class PrefeidadeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prefeidade
        fields = '__all__'
