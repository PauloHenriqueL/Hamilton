from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator



apenas_numeros = RegexValidator(
    regex=r'^\d+$',
    message="Este campo deve conter apenas números."
)

def validate_cpf(value):
    from django.core.exceptions import ValidationError
    
    # Remove qualquer formatação que possa ter
    cpf = ''.join(filter(str.isdigit, value))
    
    # Verifica se tem 11 dígitos
    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido.')
    
    # Calcula o primeiro dígito verificador
    soma = 0
    for i in range(9):
        soma += int(cpf[i]) * (10 - i)
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto
    
    # Verifica o primeiro dígito verificador
    if digito1 != int(cpf[9]):
        raise ValidationError('CPF inválido.')
    
    # Calcula o segundo dígito verificador
    soma = 0
    for i in range(10):
        soma += int(cpf[i]) * (11 - i)
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto
    
    # Verifica o segundo dígito verificador
    if digito2 != int(cpf[10]):
        raise ValidationError('CPF inválido.')

class Setor(models.Model):
    pk_setor = models.AutoField(primary_key=True, verbose_name="ID")
    setor = models.CharField(max_length=30, verbose_name="Setor")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return self.setor

    class Meta:
        db_table = '"staff"."setor"'
        verbose_name = "Setor"
        verbose_name_plural = "Setores"

class Associado(models.Model):
    pk_associado = models.AutoField(primary_key=True, verbose_name="ID")
    nome = models.CharField(max_length=255, verbose_name="Nome completo")
    email = models.EmailField(unique=True, verbose_name="E-mail")
    telefone = models.CharField(
        max_length=20, 
        verbose_name="Telefone", 
        help_text="Exemplo: 31988553344 Não coloque +55/espaços/parênteses",
        validators=[
            apenas_numeros,
            MinLengthValidator(10, "Telefone deve ter no mínimo 10 dígitos."),
        ]
    )
    cpf = models.CharField(
        max_length=11, 
        verbose_name="CPF", 
        help_text="Exemplo: 12345678901 Não coloque pontos ou traços",
        validators=[
            apenas_numeros,
            MinLengthValidator(11, "CPF deve ter 11 dígitos."),
            validate_cpf,
        ]
    )
    fk_setor = models.ForeignKey(Setor, on_delete=models.CASCADE, related_name='Setor')
    dat_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereço",
        help_text="Formato: Cidade, Rua, N° (Exemplo: Belo Horizonte, Rua Mayrink, 44)",
        validators=[
            RegexValidator(
                regex=r'^.+,\s*.+,\s*\d+$',
                message="O endereço deve seguir o formato: Cidade, Rua, Número (Exemplo: Belo Horizonte, Rua Mayrink, 44)"
            )
        ]
    )
    dif = models.TextField(null=True, blank=True, verbose_name="Diferencias")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"staff"."associado"'
        ordering = ['nome']
        verbose_name = "Associado"
        verbose_name_plural = "Associados"
    
    def __str__(self):
        return self.nome