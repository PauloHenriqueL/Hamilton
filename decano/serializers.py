from rest_framework import serializers
from decano.models import Decano


class DecanoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Decano
        fields = '__all__'
