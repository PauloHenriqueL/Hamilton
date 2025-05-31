from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count, Max, Q
from .models import Decano, Paciente, Terapeuta, Consulta, Avaliacao, Altadesistencia
from django.utils import timezone
from datetime import timedelta

# Base Admin com funcionalidades comuns
class BaseAdmin(admin.ModelAdmin):
    """Admin base com funcionalidades comuns"""
    readonly_fields = ('created_at', 'updated_at')
    
    def get_readonly_fields(self, request, obj=None):
        return self.readonly_fields if obj else ()

# Filtros reutilizáveis
class StatusFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'
    
    def lookups(self, request, model_admin):
        return [
            ('active', 'Ativos'),
            ('inactive', 'Inativos'),
            ('all', 'Todos')
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        elif self.value() == 'inactive':
            return queryset.filter(is_active=False)
        # Se value() for 'all' ou None, retorna todos os registros
        return queryset

class PeriodoFilter(admin.SimpleListFilter):
    title = 'Período'
    parameter_name = 'periodo'
    
    def lookups(self, request, model_admin):
        return [
            ('hoje', 'Hoje'),
            ('semana', 'Esta Semana'),
            ('mes', 'Este Mês'),
        ]
    
    def queryset(self, request, queryset):
        hoje = timezone.now().date()
        if self.value() == 'hoje':
            return queryset.filter(dat_consulta=hoje)
        elif self.value() == 'semana':
            inicio = hoje - timedelta(days=hoje.weekday())
            return queryset.filter(dat_consulta__range=[inicio, inicio + timedelta(days=6)])
        elif self.value() == 'mes':
            return queryset.filter(dat_consulta__year=hoje.year, dat_consulta__month=hoje.month)

# Métodos utilitários
def status_badge(valor, true_text="Ativo", false_text="Inativo"):
    """Cria badge colorido para status"""
    if valor:
        return format_html('<span style="color:green;font-weight:bold;">✓ {}</span>', true_text)
    return format_html('<span style="color:red;font-weight:bold;">✗ {}</span>', false_text)

# Admins Simplificados
@admin.register(Decano)
class DecanoAdmin(BaseAdmin):
    list_display = ['nome', 'email', 'telefone', 'status_display', 'created_at']
    list_filter = [StatusFilter]
    search_fields = ['nome', 'email', 'telefone']
    date_hierarchy = 'created_at'
    
    def status_display(self, obj):
        return status_badge(obj.is_active)
    status_display.short_description = 'Status'

@admin.register(Paciente)
class PacienteAdmin(BaseAdmin):
    list_display = ['nome', 'telefone', 'email', 'vlr_sessao', 'is_active']
    search_fields = ['nome']
    search_help_text = "Pesquise por nome do paciente"
    date_hierarchy = 'created_at'
    list_per_page = 25
    ordering = ['nome']
    
    


@admin.register(Terapeuta)
class TerapeutaAdmin(BaseAdmin):
    list_display = ['nome', 'email', 'abordagem_display', 'clinica_display', 'status_display', 'total_pacientes', 'total_consultas']
    list_filter = [StatusFilter, 'fk_abordagem', 'fk_clinica', 'sexo']
    search_fields = ['nome', 'email', 'telefone']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'fk_abordagem', 'fk_clinica'
        ).annotate(
            total_consultas=Count('consulta'),
            total_pacientes=Count('consulta__fk_paciente', distinct=True)
        )
    
    def status_display(self, obj):
        return status_badge(obj.is_active)
    status_display.short_description = 'Status'
    
    def abordagem_display(self, obj):
        return obj.fk_abordagem.abordagem if obj.fk_abordagem else '-'
    abordagem_display.short_description = 'Abordagem'
    
    def clinica_display(self, obj):
        return obj.fk_clinica.clinica if obj.fk_clinica else '-'
    clinica_display.short_description = 'Clínica'
    
    def total_pacientes(self, obj):
        return obj.total_pacientes or 0
    total_pacientes.short_description = 'Pacientes'
    
    def total_consultas(self, obj):
        return obj.total_consultas or 0
    total_consultas.short_description = 'Consultas'

@admin.register(Consulta)
class ConsultaAdmin(BaseAdmin):
    list_display = ['dat_consulta', 'paciente_nome', 'terapeuta_nome', 'vlr_consulta', 'status_realizacao', 'status_pagamento']
    list_filter = [PeriodoFilter, 'is_realizado', 'is_pago']
    search_fields = ['fk_paciente__nome', 'fk_terapeuta__nome']
    date_hierarchy = 'dat_consulta'
    list_per_page = 30
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('fk_terapeuta', 'fk_paciente')
    
    def paciente_nome(self, obj):
        return obj.fk_paciente.nome if obj.fk_paciente else '-'
    paciente_nome.short_description = 'Paciente'
    paciente_nome.admin_order_field = 'fk_paciente__nome'
    
    def terapeuta_nome(self, obj):
        return obj.fk_terapeuta.nome if obj.fk_terapeuta else '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def status_realizacao(self, obj):
        if obj.is_realizado is None:
            return format_html('<span style="color:gray;">? Indefinido</span>')
        return status_badge(obj.is_realizado, "Realizada", "Pendente")
    status_realizacao.short_description = 'Realização'
    
    def status_pagamento(self, obj):
        if obj.is_pago is None:
            return format_html('<span style="color:gray;">? Indefinido</span>')
        return status_badge(obj.is_pago, "Paga", "Pendente")
    status_pagamento.short_description = 'Pagamento'

@admin.register(Avaliacao)
class AvaliacaoAdmin(BaseAdmin):
    list_display = ['paciente_nome', 'terapeuta_nome', 'dat_consulta', 'momento', 'created_at']
    list_filter = ['momento', 'consentimento_paciente', 'continuar_terapeuta']
    search_fields = ['fk_paciente__nome', 'fk_terapeuta__nome']
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('fk_terapeuta', 'fk_paciente')
    
    def paciente_nome(self, obj):
        return obj.fk_paciente.nome if obj.fk_paciente else '-'
    paciente_nome.short_description = 'Paciente'
    
    def terapeuta_nome(self, obj):
        return obj.fk_terapeuta.nome if obj.fk_terapeuta else '-'
    terapeuta_nome.short_description = 'Terapeuta'

@admin.register(Altadesistencia)
class AltadesistenciaAdmin(BaseAdmin):
    list_display = ['paciente_nome', 'terapeuta_nome', 'alta_desistencia', 'dat_sessao', 'momento']
    list_filter = ['alta_desistencia', 'momento']
    search_fields = ['fk_paciente__nome', 'fk_terapeuta__nome']
    date_hierarchy = 'dat_sessao'
    list_per_page = 30
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('fk_terapeuta', 'fk_paciente')
    
    def paciente_nome(self, obj):
        return obj.fk_paciente.nome if obj.fk_paciente else '-'
    paciente_nome.short_description = 'Paciente'
    
    def terapeuta_nome(self, obj):
        return obj.fk_terapeuta.nome if obj.fk_terapeuta else '-'
    terapeuta_nome.short_description = 'Terapeuta'