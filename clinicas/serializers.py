from rest_framework import serializers
from clinicas.models import Clinica


class ClinicaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Clinica
        fields = '__all__'
