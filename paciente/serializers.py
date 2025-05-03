from rest_framework import serializers
from paciente.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente
        fields = '__all__'
