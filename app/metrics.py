from django.db.models import Sum, Count, F, Q, Avg, Case, When, IntegerField, DecimalField
from django.db.models.functions import TruncMonth
from django.utils.formats import number_format
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
from principais import models


def get_consulta_metrics():
    """Obter métricas gerais sobre consultas - OTIMIZADA"""
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)
    
    # UMA query para todas as métricas de consulta
    consulta_stats = models.Consulta.objects.aggregate(
        total_consultas=Count('pk_consulta'),
        consultas_realizadas=Count('pk_consulta', filter=Q(is_realizado=True)),
        consultas_pagas=Count('pk_consulta', filter=Q(is_pago=True)),
        consultas_pendentes=Count('pk_consulta', filter=Q(is_realizado=False) | Q(is_realizado=None)),
        valor_total_consultas=Sum('vlr_consulta'),
        valor_total_recebido=Sum('vlr_pago', filter=Q(is_pago=True)),
        preco_medio_esperado=Avg('fk_paciente__vlr_sessao'),
        total_sessoes_mes=Count('pk_consulta', filter=Q(
            dat_consulta__gte=primeiro_dia_mes,
            is_realizado=True
        )),
        receita_total_mes=Sum('vlr_pago', filter=Q(
            dat_consulta__gte=primeiro_dia_mes,
            is_pago=True
        ))
    )
    
    # UMA query para métricas de pacientes
    paciente_stats = models.Paciente.objects.aggregate(
        preco_medio_acordado=Avg('vlr_sessao', filter=Q(is_active=True)),
        pacientes_ativos_count=Count('pk_paciente', filter=Q(is_active=True)),
        vendas_mes=Count('pk_paciente', filter=Q(
            created_at__gte=timezone.make_aware(datetime.combine(primeiro_dia_mes, datetime.min.time()))
        ))
    )
    
    # Receita acordada em uma query
    receita_acordada = models.Consulta.objects.select_related('fk_paciente').aggregate(
        total=Sum('fk_paciente__vlr_sessao')
    )['total'] or Decimal('0.00')
    
    total_terapeutas = models.Terapeuta.objects.count()
    
    # Cálculos
    total_consultas = consulta_stats['total_consultas'] or 0
    consultas_realizadas = consulta_stats['consultas_realizadas'] or 0
    valor_total_recebido = consulta_stats['valor_total_recebido'] or Decimal('0.00')
    
    taxa_adesao = (consultas_realizadas / total_consultas * 100) if total_consultas > 0 else 0
    preco_medio_realizado = (valor_total_recebido / consultas_realizadas) if consultas_realizadas > 0 else Decimal('0.00')

    return {
        'total_consultas': total_consultas,
        'consultas_realizadas': consultas_realizadas,
        'consultas_pagas': consulta_stats['consultas_pagas'] or 0,
        'consultas_pendentes': consulta_stats['consultas_pendentes'] or 0,
        'valor_total_consultas': number_format(consulta_stats['valor_total_consultas'] or 0, decimal_pos=2, force_grouping=True),
        'valor_total_recebido': number_format(valor_total_recebido, decimal_pos=2, force_grouping=True),
        'preco_medio_acordado': number_format(paciente_stats['preco_medio_acordado'] or 0, decimal_pos=2, force_grouping=True),
        'preco_medio_esperado': number_format(consulta_stats['preco_medio_esperado'] or 0, decimal_pos=2, force_grouping=True),
        'preco_medio_realizado': number_format(preco_medio_realizado, decimal_pos=2, force_grouping=True),
        'receita_realizada': number_format(valor_total_recebido, decimal_pos=2, force_grouping=True),
        'receita_esperada': number_format(consulta_stats['valor_total_consultas'] or 0, decimal_pos=2, force_grouping=True),
        'receita_acordada': number_format(receita_acordada, decimal_pos=2, force_grouping=True),
        'taxa_adesao': number_format(taxa_adesao, decimal_pos=1),
        'total_sessoes': consultas_realizadas,
        'total_sessoes_mes': consulta_stats['total_sessoes_mes'] or 0,
        'vendas_mes': paciente_stats['vendas_mes'] or 0,
        'pacientes_ativos_count': paciente_stats['pacientes_ativos_count'] or 0,
        'total_terapeutas': total_terapeutas,
        'receita_total_mes': number_format(consulta_stats['receita_total_mes'] or 0, decimal_pos=2, force_grouping=True),
    }

def get_terapeuta_metrics():
    """Obter métricas de consultas por terapeuta - OTIMIZADA"""
    # UMA query com todas as agregações por terapeuta
    terapeutas_stats = models.Terapeuta.objects.annotate(
        total_consultas=Count('consulta'),
        total_consultasrealizadas=Count('consulta', filter=Q(consulta__is_realizado=True)),
        pacientes_ativos=Count('consulta__fk_paciente', distinct=True),
        valor_recebido=Sum('consulta__vlr_pago', filter=Q(consulta__is_pago=True)),
        receita_esperada=Sum('consulta__vlr_consulta')
    ).values(
        'nome',
        'total_consultas',
        'total_consultasrealizadas', 
        'pacientes_ativos',
        'valor_recebido',
        'receita_esperada'
    )
    
    metricas_detalhadas = []
    for stats in terapeutas_stats:
        total_consultas = stats['total_consultas'] or 0
        total_realizadas = stats['total_consultasrealizadas'] or 0
        valor_recebido = stats['valor_recebido'] or Decimal('0.00')
        receita_esperada = stats['receita_esperada'] or Decimal('0.00')
        
        taxa_adesao = (total_realizadas / total_consultas * 100) if total_consultas > 0 else 0
        diferenca = valor_recebido - receita_esperada
        status_diferenca = "positivo" if diferenca > 0 else ("negativo" if diferenca < 0 else "igual")
        
        metricas_detalhadas.append({
            'nome': stats['nome'],
            'taxa_adesao': number_format(taxa_adesao, decimal_pos=1),
            'pacientes_ativos': stats['pacientes_ativos'] or 0,
            'total_consultas': total_consultas,
            'total_consultasrealizadas': total_realizadas,
            'valor_recebido': number_format(valor_recebido, decimal_pos=2, force_grouping=True),
            'receita_esperada': number_format(receita_esperada, decimal_pos=2, force_grouping=True),
            'diferenca': number_format(diferenca, decimal_pos=2, force_grouping=True),
            'status_diferenca': status_diferenca
        })
    
    return metricas_detalhadas

def get_daily_consultas_data():
    """Obter dados diários de consultas - OTIMIZADA"""
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # UMA query para todos os dias
    daily_stats = models.Consulta.objects.filter(
        dat_consulta__in=last_7_days
    ).values('dat_consulta').annotate(
        consultas_count=Count('pk_consulta')
    ).order_by('dat_consulta')
    
    # Criar dicionário para lookup rápido
    daily_dict = {str(item['dat_consulta']): item['consultas_count'] for item in daily_stats}
    
    return {
        'dates': [str(date) for date in last_7_days],
        'values': [daily_dict.get(str(date), 0) for date in last_7_days]
    }

def get_monthly_consultas_data():
    """Obter dados mensais de consultas - OTIMIZADA"""
    today = timezone.now().date()
    six_months_ago = today - timedelta(days=180)
    
    # UMA query para todos os meses
    monthly_stats = models.Consulta.objects.filter(
        dat_consulta__gte=six_months_ago
    ).annotate(
        month=TruncMonth('dat_consulta')
    ).values('month').annotate(
        consultas_count=Count('pk_consulta')
    ).order_by('month')
    
    return {
        'months': [item['month'].strftime('%b/%Y') for item in monthly_stats],
        'values': [item['consultas_count'] for item in monthly_stats]
    }

def get_monthly_receita_data():
    """Obter dados mensais de receita - OTIMIZADA"""
    today = timezone.now().date()
    six_months_ago = today - timedelta(days=180)
    
    # UMA query para todos os meses
    monthly_stats = models.Consulta.objects.filter(
        dat_consulta__gte=six_months_ago,
        is_pago=True
    ).annotate(
        month=TruncMonth('dat_consulta')
    ).values('month').annotate(
        receita_total=Sum('vlr_pago')
    ).order_by('month')
    
    return {
        'months': [item['month'].strftime('%b/%Y') for item in monthly_stats],
        'values': [float(item['receita_total'] or 0) for item in monthly_stats]
    }

def get_daily_valor_data():
    """Obter dados diários de valor - OTIMIZADA"""
    today = timezone.now().date()
    last_7_days = [today - timedelta(days=i) for i in range(6, -1, -1)]
    
    # UMA query para todos os dias
    daily_stats = models.Consulta.objects.filter(
        dat_consulta__in=last_7_days
    ).values('dat_consulta').annotate(
        valor_total=Sum('vlr_consulta')
    ).order_by('dat_consulta')
    
    # Criar dicionário para lookup rápido
    daily_dict = {str(item['dat_consulta']): float(item['valor_total'] or 0) for item in daily_stats}
    
    return {
        'dates': [str(date) for date in last_7_days],
        'values': [daily_dict.get(str(date), 0) for date in last_7_days]
    }

def get_consultas_por_status():
    """Obter contagem de consultas por status - OTIMIZADA"""
    # UMA query para todos os status
    status_stats = models.Consulta.objects.aggregate(
        total_pagas=Count('pk_consulta', filter=Q(is_pago=True)),
        total_nao_pagas=Count('pk_consulta', filter=Q(is_pago=False) | Q(is_pago=None)),
        total_realizadas=Count('pk_consulta', filter=Q(is_realizado=True)),
        total_nao_realizadas=Count('pk_consulta', filter=Q(is_realizado=False) | Q(is_realizado=None))
    )
    
    return {
        'pagamento_status_data': {
            'pago': status_stats['total_pagas'],
            'pendente': status_stats['total_nao_pagas']
        },
        'realizacao_status_data': {
            'realizada': status_stats['total_realizadas'],
            'nao_realizada': status_stats['total_nao_realizadas']
        }
    }

def get_pacientes_ativos():
    """Obter pacientes com mais consultas - OTIMIZADA"""
    # UMA query para os top 5 pacientes
    top_pacientes = models.Paciente.objects.annotate(
        consultas_count=Count('consulta')
    ).filter(
        consultas_count__gt=0
    ).order_by('-consultas_count')[:5].values('nome', 'consultas_count')
    
    return {item['nome']: item['consultas_count'] for item in top_pacientes}