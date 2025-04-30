from rest_framework import serializers
from paciente.models import Paciente


class PacienteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Paciente
        fields = [
            'nome',
            'usuario',
            'email',
            'telefone',
            'contato_apoio',
            'dat_nascimento',
            'vlr_sessao',
            'qtd_sessao',
            'fk_captacao'
        ]
