from rest_framework import serializers
from fistkiss.models import Firstkiss


class FirstkissSerializer(serializers.ModelSerializer):

    class Meta:
        model = Firstkiss
        fields = '__all__'
