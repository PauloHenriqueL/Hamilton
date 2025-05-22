from django import forms
from . import models
import re
from django.core.exceptions import ObjectDoesNotExist


class ConsultaForm(forms.ModelForm):
    
    class Meta:
        model = models.Consulta
        fields = [
            'fk_terapeuta', 
            'fk_paciente', 
            'vlr_consulta',
            'is_realizado',  
            'is_pago', 
            'vlr_pago',
            'dat_consulta',  # Adicionando o campo de data
        ]
        widgets = {
            'fk_terapeuta': forms.Select(attrs={'class': 'form-control'}),
            'fk_paciente': forms.Select(attrs={'class': 'form-control', 'id': 'paciente-select'}),
            'vlr_consulta': forms.NumberInput(attrs={'class': 'form-control', 'id': 'valor-consulta'}),
            'is_realizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vlr_pago': forms.NumberInput(attrs={'class': 'form-control'}),
            'dat_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        labels = {
            'fk_terapeuta': 'Terapeuta', 
            'fk_paciente': 'Paciente', 
            'vlr_consulta': 'Valor da consulta',
            'is_realizado': 'Foi realizado?',  
            'is_pago': 'Foi pago?', 
            'vlr_pago': 'Valor pago?',
            'dat_consulta': 'Data da consulta'
        }

    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    vlr_pix_total = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        label='Valor total recebido no PIX'
    )
    
    # Campo oculto para manter o valor do terapeuta quando o campo estiver disabled
    terapeuta_hidden = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Se o formulário for preenchido com dados POST e tiver paciente selecionado
        if args and isinstance(args[0], dict) and 'fk_paciente' in args[0]:
            paciente_id = args[0].get('fk_paciente')
            if paciente_id:
                try:
                    paciente = models.Paciente.objects.get(pk=paciente_id)
                    self.fields['vlr_consulta'].initial = paciente.vlr_sessao
                except ObjectDoesNotExist:
                    pass
    
    def clean(self):
        cleaned_data = super().clean()
        vlr_consulta = cleaned_data.get('vlr_consulta')
        vlr_pago = cleaned_data.get('vlr_pago')
        is_realizado = cleaned_data.get('is_realizado')
        is_pago = cleaned_data.get('is_pago')
        
        # Validação de valores positivos
        if vlr_consulta is not None and vlr_consulta <= 0:
            self.add_error('vlr_consulta', 'O valor da consulta deve ser positivo.')
        
        if vlr_pago is not None and vlr_pago < 0:
            self.add_error('vlr_pago', 'O valor pago não pode ser negativo.')
        
        # Consultas não realizadas não podem estar pagas
        if is_realizado is False and is_pago is True:
            self.add_error('is_pago', 'Uma consulta não realizada não pode estar paga.')
        
        return cleaned_data