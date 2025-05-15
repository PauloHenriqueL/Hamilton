from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator
from nucleo.models import Nucleo


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
    faculdade = models.CharField(null=True,blank=True,max_length=255, verbose_name="Faculdade")
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
    telefone_eme = models.CharField(
        null=True,
        blank=True,
        max_length=20, 
        verbose_name="Telefone de emergência", 
        help_text="Exemplo: 31988553344 Não coloque +55/espaços/parênteses",
        validators=[
            apenas_numeros,
            MinLengthValidator(10, "Telefone deve ter no mínimo 10 dígitos."),
        ]
    )
    fk_nucleo = models.ForeignKey(
        Nucleo,
        null=True,
        blank=True,
        on_delete=models.CASCADE, 
        db_column='fk_nucleo',
        verbose_name="Núcleo"
    )
    cpf = models.CharField(
        null=True,
        blank=True,
        max_length=11, 
        verbose_name="CPF", 
        help_text="Exemplo: 12345678901 Não coloque pontos ou traços",
        validators=[
            apenas_numeros,
            MinLengthValidator(11, "CPF deve ter 11 dígitos."),
            validate_cpf,
        ]
    )
    fk_setores = models.ManyToManyField(
        Setor, 
        through='AssociadoSetor',
        related_name='associados', 
        verbose_name="Setores"
    )
    dat_nascimento = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    sexo = models.CharField(
        max_length=1, 
        choices=[('M', 'Masculino'), ('F', 'Feminino'), ('O', 'Outro')],
        verbose_name="Sexo"
    )
    endereco = models.CharField(
        max_length=255,
        verbose_name="Endereço",
        help_text="Formato: Estado, Cidade (Exemplo: MG, Belo Horizonte)",
        validators=[
            RegexValidator(
                regex=r'^[A-Z]{2},\s*[A-Za-zÀ-ÿ\s]+$',
                message="O endereço deve seguir o formato: Estado, Cidade (Exemplo: MG, Belo Horizonte)"
            )
        ]
    )
    rem = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="Remuneração")
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    is_pcd = models.BooleanField(default=True, verbose_name="PCD")
    dif = models.TextField(null=True, blank=True, verbose_name="Diferencias")
    rep = models.TextField(null=True, blank=True, verbose_name="Responsabilidades")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"staff"."associado"'
        ordering = ['nome']
        verbose_name = "Associado"
        verbose_name_plural = "Associados"
    
    def __str__(self):
        return self.nome

class AssociadoSetor(models.Model):
    associado = models.ForeignKey(
        Associado,
        on_delete=models.CASCADE,
        db_column='associado_id'
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.CASCADE,
        db_column='setor_id'
    )
    
    class Meta:
        db_table = '"staff"."associado_setor"'
        unique_together = (('associado', 'setor'),)
        verbose_name = "Associação Associado-Setor"
        verbose_name_plural = "Associações Associado-Setor"
