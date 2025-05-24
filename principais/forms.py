from django import forms
from . import models
import re
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)


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
            'dat_consulta',
        ]
        widgets = {
            'fk_terapeuta': forms.Select(attrs={'class': 'form-control'}),
            'fk_paciente': forms.Select(attrs={'class': 'form-control', 'id': 'paciente-select'}),
            'vlr_consulta': forms.NumberInput(attrs={'class': 'form-control', 'id': 'valor-consulta'}),
            'is_realizado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'is_pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'vlr_pago': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'dat_consulta': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
        }
        labels = {
            'fk_terapeuta': 'Terapeuta', 
            'fk_paciente': 'Paciente', 
            'vlr_consulta': 'Valor da consulta',
            'is_realizado': 'Foi realizada?',  
            'is_pago': 'Foi paga?', 
            'vlr_pago': 'Valor pago',
            'dat_consulta': 'Data da consulta'
        }

    quantidade = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'value': '1'}),
        required=False,
        label='Quantidade de consultas'
    )
    
    vlr_pix_total = forms.DecimalField(
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        label='Valor total recebido no PIX'
    )
    
    # Campo oculto para manter o valor do terapeuta quando o campo estiver disabled
    terapeuta_hidden = forms.IntegerField(required=False, widget=forms.HiddenInput())
    
    def __init__(self, *args, **kwargs):
        # Extrair parâmetros customizados antes de chamar super()
        user_terapeuta = kwargs.pop('user_terapeuta', None)
        super().__init__(*args, **kwargs)
        
        logger.info(f"Inicializando formulário. user_terapeuta: {user_terapeuta}")
        
        # Se um terapeuta foi passado para o formulário, configurar os campos
        if user_terapeuta:
            logger.info(f"Configurando terapeuta: {user_terapeuta.pk_terapeuta} - {user_terapeuta.nome}")
            
            # Definir o valor inicial e desabilitar o campo
            self.fields['fk_terapeuta'].initial = user_terapeuta.pk_terapeuta
            self.fields['fk_terapeuta'].widget.attrs.update({
                'disabled': 'disabled',
                'readonly': 'readonly'
            })
            
            # Definir o campo oculto
            self.fields['terapeuta_hidden'].initial = user_terapeuta.pk_terapeuta
            
            # IMPORTANTE: Marcar o campo como não obrigatório quando desabilitado
            # pois campos disabled não são enviados no POST
            self.fields['fk_terapeuta'].required = False
            
            logger.info(f"Campo terapeuta configurado. Initial: {self.fields['fk_terapeuta'].initial}, Hidden: {self.fields['terapeuta_hidden'].initial}")
        
        # Se o formulário for preenchido com dados POST e tiver paciente selecionado
        if args and isinstance(args[0], dict) and 'fk_paciente' in args[0]:
            paciente_id = args[0].get('fk_paciente')
            if paciente_id:
                try:
                    paciente = models.Paciente.objects.get(pk=paciente_id)
                    self.fields['vlr_consulta'].initial = paciente.vlr_sessao
                    logger.info(f"Valor da consulta definido automaticamente: {paciente.vlr_sessao}")
                except ObjectDoesNotExist:
                    logger.warning(f"Paciente com ID {paciente_id} não encontrado")
    
    def clean(self):
        cleaned_data = super().clean()
        vlr_consulta = cleaned_data.get('vlr_consulta')
        vlr_pago = cleaned_data.get('vlr_pago')
        is_realizado = cleaned_data.get('is_realizado')
        is_pago = cleaned_data.get('is_pago')
        
        logger.info(f"Iniciando clean(). Data recebida: {dict(self.data)}")
        
        # CORREÇÃO PRINCIPAL: Se o campo terapeuta estiver desabilitado ou vazio, usar o valor do campo oculto
        terapeuta_hidden_value = self.data.get('terapeuta_hidden')
        
        if terapeuta_hidden_value:
            logger.info(f"Usando valor do campo oculto: {terapeuta_hidden_value}")
            try:
                terapeuta_id = int(terapeuta_hidden_value)
                terapeuta = models.Terapeuta.objects.get(pk=terapeuta_id)
                cleaned_data['fk_terapeuta'] = terapeuta
                logger.info(f"Terapeuta definido via campo oculto: {terapeuta}")
            except (ValueError, TypeError, models.Terapeuta.DoesNotExist) as e:
                logger.error(f"Erro ao processar terapeuta_hidden: {e}")
                self.add_error('fk_terapeuta', 'Terapeuta inválido.')
        
        # Se ainda não há terapeuta no cleaned_data, é um erro
        if not cleaned_data.get('fk_terapeuta'):
            logger.error("Nenhum terapeuta foi definido")
            self.add_error('fk_terapeuta', 'O campo terapeuta é obrigatório.')
        else:
            logger.info(f"Terapeuta final: {cleaned_data.get('fk_terapeuta')}")
        
        # Validação de valores positivos
        if vlr_consulta is not None and vlr_consulta <= 0:
            self.add_error('vlr_consulta', 'O valor da consulta deve ser positivo.')
        
        if vlr_pago is not None and vlr_pago < 0:
            self.add_error('vlr_pago', 'O valor pago não pode ser negativo.')
        
        # Consultas não realizadas não podem estar pagas
        if is_realizado is False and is_pago is True:
            self.add_error('is_pago', 'Uma consulta não realizada não pode estar paga.')
        
        logger.info(f"Clean finalizado. Cleaned_data: {cleaned_data}")
        return cleaned_data