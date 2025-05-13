from rest_framework import serializers
from lastkiss.models import Lastkiss


class LastkissSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lastkiss
        fields = '__all__'
