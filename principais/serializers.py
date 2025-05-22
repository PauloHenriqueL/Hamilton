from rest_framework import serializers
from acessorios.models import Abordagem, Nucleo, Clinica, Modalidade, Captacao
from . import models


class ConsultaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Consulta
        fields = '__all__'

class DecanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Decano
        fields = '__all__'

class TerapeutaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Terapeuta
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Paciente
        fields = '__all__'

class FirstkissSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Firstkiss
        fields = '__all__'


class LastkissSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Lastkiss
        fields = '__all__'


class AltadesistenciaSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Altadesistencia
        fields = '__all__'