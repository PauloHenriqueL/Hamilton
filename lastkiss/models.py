from django.db import models
from decano.models import Decano
from terapeuta.models import Terapeuta
from paciente.models import Paciente
from django.core.validators import MinValueValidator, MaxValueValidator


class Lastkiss(models.Model):
    pk_lastkiss = models.AutoField(primary_key=True, verbose_name="ID")
    fk_decano = models.ForeignKey(
        Decano, 
        on_delete=models.CASCADE, 
        db_column='fk_decano',
        verbose_name="Decano"
    )
    fk_terapeuta = models.ForeignKey(
        Terapeuta, 
        on_delete=models.CASCADE, 
        db_column='fk_terapeuta',
        verbose_name="Terapeuta"
    )
    fk_paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.CASCADE, 
        db_column='fk_paciente',
        verbose_name="Paciente"
    )

    consentimento_paciente = models.CharField(
        null=True,
        blank=True,
        verbose_name="Paciente consente com a pesquisa?",
        choices=[('S', 'Sim'), ('N', 'Não')]     
    )

    bem_estar = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nível de Bem Estar pessoal (1-10)",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    interpessoal = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nível de Relacionamentos Interpessoais (1-10)",
        help_text="familia/relacionamentos intimos",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    social = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nível dos Relacionamentos Pessoias (1-10)",
        help_text="trabalho/faculdade/amigos",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    geral = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Estado geral de bem estar (1-10)",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    acolhimento = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nível de Acolhimento (1-10)",
        help_text="Quanto me senti ouvido/comprendido ou respeitado",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    abordagem = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Abordagem (1-10)",
        help_text="Quanto sinto que a abordagem combina comigo",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    nivel_expectativa = models.IntegerField(
        null=True,
        blank=True,
        verbose_name="Nível de Expectativa (1-10)",
        help_text="1 = Sinto que a abordagem do terapeuta não combina comigo, 10 = Sinto que a abordagem combina comigo",
        validators=[
            MinValueValidator(1, message="O valor mínimo é 1"),
            MaxValueValidator(10, message="O valor máximo é 10")
        ]
    )

    desejo = models.CharField(
        null=True,
        blank=True,
        verbose_name="Paciente deseja realizar a terapia com outro terapeuta?",
        choices=[('S', 'Sim'), ('N', 'Não')]     
    )

    recomendaria = models.CharField(
        null=True,
        blank=True,
        verbose_name="Paciente recomendaria a Allos?",
        choices=[('S', 'Sim'), ('N', 'Não')]     
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    class Meta:
        db_table = '"hamilton"."lastkiss"'
        verbose_name = "Lastkiss"
        verbose_name_plural = "Lastkiss"