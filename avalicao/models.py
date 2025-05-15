# avaliacao/models.py
from django.db import models
from django.contrib.auth.models import User  # Importe o modelo User


class Avaliador(models.Model):
    pk_avaliador = models.AutoField(primary_key=True, verbose_name='ID')
    nome = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = '"staff"."avaliador"'
        verbose_name = 'Avaliador'
        verbose_name_plural = 'Avaliadores'

class Avaliado(models.Model):
    pk_avaliado = models.AutoField(primary_key=True, verbose_name='ID')
    nome = models.CharField(max_length=200, verbose_name='Nome completo')
    is_associate = models.BooleanField(default=False, verbose_name='É associado')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Data de Atualização")

    def __str__(self):
        return self.nome
    
    class Meta:
        db_table = '"staff"."avaliado"'
        verbose_name = 'Avaliado'
        verbose_name_plural = 'Avaliados'


class Avaliacao(models.Model):
    pk_avaliacao = models.AutoField(primary_key=True, verbose_name='ID')
    fk_avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='Availicaos')
    fk_avaliado = models.ForeignKey(Avaliado, on_delete=models.CASCADE, related_name='Availicaos')
    dat_avaliacao  = models.DateField(verbose_name="Data da Avalicao")

    SCORE_CHOICES = [
        (-9, '-9'),
        (-3, '-3'),
        (-1, '-1'),
        (0, '0'),
        (1, '+1'),
        (3, '+3'),      
        (9, '+9'),
    ]

    estagio_mudanca = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Estágio de Mudança")
    estrutura = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Estruturação da Sessão")
    encerramento = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Qualidade do Encerramento")
    acolhimento = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Nível de Acolhimento")
    seguranca_terapeuta = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Segurança Transmitida pelo Terapeuta")
    seguranca_metodo = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Segurança no Método Aplicado")
    aprofundar = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Capacidade de Aprofundamento")
    hipoteses = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Formulação de Hipóteses")
    interpretativa = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Capacidade Interpretativa")
    frase_timing = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Timing e Qualidade das Frases")
    corpo_setting = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Atenção ao Corpo e Setting")
    insight_potencia = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Potência de Insights Gerados")
    
    def __str__(self):
        return f"Availiallos do {self.fk_avaliado} pelo {self.fk_avaliador}"
    
    def get_avg_score(self):
        """Calcula a pontuação média de todos os critérios de avaliação"""
        scores = [
            self.estagio_mudanca, self.estrutura, self.encerramento, 
            self.acolhimento, self.seguranca_terapeuta, self.seguranca_metodo,
            self.aprofundar, self.hipoteses, self.interpretativa,
            self.frase_timing, self.corpo_setting, self.insight_potencia
        ]
        return sum(scores) / len(scores)
    
    class Meta:
        db_table = '"staff"."avaliacao"'
        verbose_name = 'Availiallos'
        verbose_name_plural = 'Availiallos'
        ordering = ['-dat_avaliacao']  


class Avalioracao(models.Model):
    pk_avalioracao = models.AutoField(primary_key=True, verbose_name='ID')
    fk_avaliador = models.ForeignKey(Avaliador, on_delete=models.CASCADE, related_name='Oracao')
    fk_avaliado = models.ForeignKey(Avaliado, on_delete=models.CASCADE, related_name='Oracao')
    dat_avaliacao  = models.DateField(verbose_name="Data da Avalicao")

    SCORE_CHOICES = [
        (-9, '-9'),
        (-3, '-3'),
        (-1, '-1'),
        (0, '0'),
        (1, '+1'),
        (3, '+3'),      
        (9, '+9'),
    ]

    profundidade = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Profundidade")
    domínio_vocabular = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Domínio Vocabular")
    estrutura_didatica = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Estrutura Didática")
    presenca = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Presença")
    cultura_repertorio = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Cultura e Repertório")
    velocidade_ritmo = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Velocidade de Raciocínio e Ritmo de Fala")
    preparacao = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Esforço / Preparação / Setting")
    carisma = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Carisma")
    opi_avaliador = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Opinião do avaliador")
    contexto = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Contexto")
    recorte = models.IntegerField(choices=SCORE_CHOICES, verbose_name="Qualidade do Recorte Temático")
    obs = models.TextField(null=True, blank=True, verbose_name="Observações")

    def __str__(self):
        return f"Availição do {self.fk_avaliado} pelo {self.fk_avaliador}"
    
    class Meta:
        db_table = '"staff"."avalioracao"'
        verbose_name = 'Avaliação de Comunicão Oral'
        verbose_name_plural = 'Availiações orais'
        ordering = ['-dat_avaliacao']