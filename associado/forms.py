from django import forms
from . import models
import re


class AssociadoForm(forms.ModelForm):
    class Meta:
        model = models.Associado
        fields = [
            'nome', 
            'email', 
            'telefone', 
            'cpf', 
            'fk_setor', 
            'dat_nascimento', 
            'endereco', 
            'dif', 
            'is_active'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'fk_setor': forms.Select(attrs={'class': 'form-control'}),
            'dat_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'dif': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
        
    def clean_cpf(self):
        """Validação adicional para o CPF"""
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) != 11:
            raise forms.ValidationError("CPF deve ter 11 dígitos.")
        return cpf
    
    def clean_telefone(self):
        """Validação adicional para o telefone"""
        telefone = self.cleaned_data.get('telefone')
        if telefone and len(telefone) < 10:
            raise forms.ValidationError("Telefone deve ter no mínimo 10 dígitos.")
        return telefone
    
    def clean_endereco(self):
        """Validação adicional para o endereço"""
        endereco = self.cleaned_data.get('endereco')
        if endereco and not re.match(r'^.+,\s*.+,\s*\d+$', endereco):
            raise forms.ValidationError(
                "O endereço deve seguir o formato: Cidade, Rua, Número (Exemplo: Belo Horizonte, Rua Mayrink, 44)"
            )
        return endereco