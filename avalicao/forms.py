from django import forms
from . import models
import re

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = models.Avaliacao
        fields = [
            'fk_avaliador',
            'fk_avaliado',
            'dat_avaliacao',
            'estagio_mudanca',
            'estrutura',
            'encerramento',
            'acolhimento',
            'seguranca_terapeuta',
            'seguranca_metodo',
            'aprofundar',
            'hipoteses',
            'interpretativa',
            'frase_timing',
            'corpo_setting',
            'insight_potencia'
        ]
        widgets = {
            'fk_avaliador': forms.Select(attrs={'class': 'form-control'}),
            'fk_avaliado': forms.Select(attrs={'class': 'form-control'}),
            'dat_avaliacao': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estagio_mudanca': forms.Select(attrs={'class': 'form-control'}),
            'estrutura': forms.Select(attrs={'class': 'form-control'}),
            'encerramento': forms.Select(attrs={'class': 'form-control'}),
            'acolhimento': forms.Select(attrs={'class': 'form-control'}),
            'seguranca_terapeuta': forms.Select(attrs={'class': 'form-control'}),
            'seguranca_metodo': forms.Select(attrs={'class': 'form-control'}),
            'aprofundar': forms.Select(attrs={'class': 'form-control'}),
            'hipoteses': forms.Select(attrs={'class': 'form-control'}),
            'interpretativa': forms.Select(attrs={'class': 'form-control'}),
            'frase_timing': forms.Select(attrs={'class': 'form-control'}),
            'corpo_setting': forms.Select(attrs={'class': 'form-control'}),
            'insight_potencia': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Adiciona classes de estilo para todos os campos de score
        score_fields = [
            'estagio_mudanca', 'estrutura', 'encerramento', 'acolhimento',
            'seguranca_terapeuta', 'seguranca_metodo', 'aprofundar', 'hipoteses',
            'interpretativa', 'frase_timing', 'corpo_setting', 'insight_potencia'
        ]
        
        for field in score_fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control score-select',
                'data-field': field
            })
            
        # Adiciona help_text aos campos
        self.fields['dat_avaliacao'].help_text = "Selecione a data em que a avaliação foi realizada"