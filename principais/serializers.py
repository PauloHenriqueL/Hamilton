from rest_framework import serializers
from . import models


class ConsultaSerializer(serializers.ModelSerializer):
    # ✅ Dados relacionados para evitar queries extras
    terapeuta_nome = serializers.CharField(source='fk_terapeuta.nome', read_only=True)
    paciente_nome = serializers.CharField(source='fk_paciente.nome', read_only=True)
    abordagem_nome = serializers.CharField(source='fk_terapeuta.fk_abordagem.abordagem', read_only=True)
    clinica_nome = serializers.CharField(source='fk_terapeuta.fk_clinica.clinica', read_only=True)

    class Meta:
        model = models.Consulta
        fields = '__all__'


class DecanoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Decano
        fields = '__all__'


class TerapeutaSerializer(serializers.ModelSerializer):
    # ✅ Estatísticas pré-calculadas (vindas das annotations)
    total_consultas = serializers.IntegerField(read_only=True)
    total_pacientes = serializers.IntegerField(read_only=True)
    
    # ✅ Dados relacionados para evitar queries extras
    abordagem_nome = serializers.CharField(source='fk_abordagem.abordagem', read_only=True)
    clinica_nome = serializers.CharField(source='fk_clinica.clinica', read_only=True)
    decano_nome = serializers.CharField(source='fk_decano.nome', read_only=True)
    nucleo_nome = serializers.CharField(source='fk_nucleo.nucleo', read_only=True)
    modalidade_nome = serializers.CharField(source='fk_modalidade.modalidade', read_only=True)

    class Meta:
        model = models.Terapeuta
        fields = '__all__'


class PacienteSerializer(serializers.ModelSerializer):
    # ✅ Dados relacionados para evitar queries extras
    clinica_nome = serializers.CharField(source='fk_clinica.clinica', read_only=True)
    modalidade_nome = serializers.CharField(source='fk_modalidade.modalidade', read_only=True)
    captacao_nome = serializers.CharField(source='fk_captacao.captacao', read_only=True)
    
    # ✅ Estatísticas pré-calculadas (vindas das annotations)
    total_consultas = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Paciente
        fields = '__all__'


class AvaliacaoSerializer(serializers.ModelSerializer):
    # ✅ Dados relacionados para evitar queries extras
    terapeuta_nome = serializers.CharField(source='fk_terapeuta.nome', read_only=True)
    paciente_nome = serializers.CharField(source='fk_paciente.nome', read_only=True)

    class Meta:
        model = models.Avaliacao
        fields = '__all__'


class AltadesistenciaSerializer(serializers.ModelSerializer):
    # ✅ Dados relacionados para evitar queries extras
    terapeuta_nome = serializers.CharField(source='fk_terapeuta.nome', read_only=True)
    paciente_nome = serializers.CharField(source='fk_paciente.nome', read_only=True)

    class Meta:
        model = models.Altadesistencia
        fields = '__all__'