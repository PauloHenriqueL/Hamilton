from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Sum, Count
from .models import Decano, Paciente, Terapeuta, Consulta, Firstkiss, Lastkiss, Altadesistencia
from django.utils import timezone
from datetime import datetime, timedelta

class IsActiveFilter(admin.SimpleListFilter):
    title = 'Status'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return (
            ('active', 'Ativos'),
            ('inactive', 'Inativos'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        if self.value() == 'inactive':
            return queryset.filter(is_active=False)


@admin.register(Decano)
class DecanoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'dat_nascimento', 'status_ativo', 'created_at')
    list_filter = (IsActiveFilter, 'created_at')
    search_fields = ('nome', 'email', 'telefone')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Pessoais', {
                'fields': ('nome', 'email', 'telefone', 'dat_nascimento')
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
        ]
        
        # Adiciona datas do sistema apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    date_hierarchy = 'created_at'
    
    def status_ativo(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;font-weight:bold;">✓ Ativo</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Inativo</span>')
    status_ativo.short_description = 'Status'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'telefone', 'email', 'vlr_sessao', 'status_ativo', 'total_consultas', 'data_ultima_consulta', 'created_at')
    list_filter = (IsActiveFilter, 'fk_captacao', 'fk_clinica', 'created_at')  # Adicionado fk_clinica
    search_fields = ('nome', 'email', 'telefone')
    readonly_fields = ('created_at', 'updated_at', 'total_consultas', 'data_ultima_consulta')
    
    def get_fieldsets(self, request, obj=None):
        # Fieldsets básicos para criação e edição
        fieldsets = [
            ('Informações Pessoais', {
                'fields': ('nome', 'email', 'telefone', 'dat_nascimento')
            }),
            ('Contato de Apoio', {
                'fields': ('nome_contato_apoio', 'parentesco_contato_apoio', 'contato_apoio'),
                'classes': ('collapse',)
            }),
            ('Informações de Cadastro', {
                'fields': ('fk_clinica', 'fk_modalidade', 'fk_captacao', 'vlr_sessao', 'oberservacao', 'is_active')  # Adicionado fk_clinica
            }),
        ]
        
        # Adiciona estatísticas e datas apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Estatísticas', {
                    'fields': ('total_consultas', 'data_ultima_consulta'),
                })
            )
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    date_hierarchy = 'created_at'
    list_per_page = 20

    def status_ativo(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;font-weight:bold;">✓ Ativo</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Inativo</span>')
    status_ativo.short_description = 'Status'
    
    def total_consultas(self, obj):
        if obj and obj.pk:
            return Consulta.objects.filter(fk_paciente=obj).count()
        return 0
    total_consultas.short_description = 'Total de Consultas'
    
    def data_ultima_consulta(self, obj):
        if obj and obj.pk:
            ultima = Consulta.objects.filter(fk_paciente=obj).order_by('-dat_consulta').first()  # Corrigido: dat_consulta
            if ultima and ultima.dat_consulta:
                return ultima.dat_consulta
        return '-'
    data_ultima_consulta.short_description = 'Última Consulta'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


@admin.register(Terapeuta)
class TerapeutaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'faculdade', 'abordagem_nome', 'clinica_nome', 'status_ativo', 'total_pacientes', 'total_consultas', 'created_at')  # Adicionado faculdade
    list_filter = (IsActiveFilter, 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 'fk_modalidade', 'sexo')
    search_fields = ('nome', 'email', 'telefone', 'faculdade')  # Adicionado faculdade
    readonly_fields = ('created_at', 'updated_at', 'total_pacientes', 'total_consultas', 'taxa_realizacao')
    
    def get_fieldsets(self, request, obj=None):
        # Fieldsets básicos para criação e edição
        fieldsets = [
            ('Informações Pessoais', {
                'fields': ('nome', 'email', 'telefone', 'dat_nascimento', 'sexo')
            }),
            ('Informações Acadêmicas', {
                'fields': ('faculdade',)  # Adicionado seção para faculdade
            }),
            ('Informações Profissionais', {
                'fields': ('fk_decano', 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 'fk_modalidade')
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
        ]
        
        # Adiciona estatísticas e datas apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Estatísticas', {
                    'fields': ('total_pacientes', 'total_consultas', 'taxa_realizacao'),
                })
            )
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    date_hierarchy = 'created_at'
    
    def status_ativo(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;font-weight:bold;">✓ Ativo</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Inativo</span>')
    status_ativo.short_description = 'Status'
    
    def abordagem_nome(self, obj):
        if obj and obj.fk_abordagem:
            return obj.fk_abordagem.abordagem
        return '-'
    abordagem_nome.short_description = 'Abordagem'
    
    def clinica_nome(self, obj):
        if obj and obj.fk_clinica:
            return obj.fk_clinica.clinica
        return '-'
    clinica_nome.short_description = 'Clínica'
    
    def total_pacientes(self, obj):
        if obj and obj.pk:
            # Conta pacientes únicos que tiveram consultas com este terapeuta
            return Consulta.objects.filter(fk_terapeuta=obj).values('fk_paciente').distinct().count()
        return 0
    total_pacientes.short_description = 'Total de Pacientes'
    
    def total_consultas(self, obj):
        if obj and obj.pk:
            return Consulta.objects.filter(fk_terapeuta=obj).count()
        return 0
    total_consultas.short_description = 'Total de Consultas'
    
    def taxa_realizacao(self, obj):
        if obj and obj.pk:
            consultas = Consulta.objects.filter(fk_terapeuta=obj)
            total = consultas.count()
            realizadas = consultas.filter(is_realizado=True).count()
            if total > 0:
                taxa = (realizadas / total) * 100
                return f"{taxa:.1f}%"
        return "N/A"
    taxa_realizacao.short_description = 'Taxa de Realização'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


class ConsultaDataFilter(admin.SimpleListFilter):
    title = 'Período'
    parameter_name = 'periodo'

    def lookups(self, request, model_admin):
        return (
            ('hoje', 'Hoje'),
            ('semana', 'Esta Semana'),
            ('mes', 'Este Mês'),
            ('pendente', 'Pendentes de Realização'),
            ('pendente_pagamento', 'Pendentes de Pagamento'),
        )

    def queryset(self, request, queryset):
        hoje = timezone.now().date()
        
        if self.value() == 'hoje':
            return queryset.filter(data=hoje)
        if self.value() == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fim_semana = inicio_semana + timedelta(days=6)
            return queryset.filter(data__range=[inicio_semana, fim_semana])
        if self.value() == 'mes':
            inicio_mes = hoje.replace(day=1)
            if hoje.month == 12:
                fim_mes = hoje.replace(year=hoje.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                fim_mes = hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1)
            return queryset.filter(data__range=[inicio_mes, fim_mes])
        if self.value() == 'pendente':
            return queryset.filter(is_realizado=False)
        if self.value() == 'pendente_pagamento':
            return queryset.filter(is_pago=False, is_realizado=True)


@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ('dat_consulta', 'paciente_nome', 'terapeuta_nome', 'vlr_consulta', 'status_realizacao', 'status_pagamento', 'vlr_pago', 'created_at')
    list_filter = (ConsultaDataFilter, 'is_realizado', 'is_pago', 'fk_terapeuta', 'fk_paciente')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente', 'dat_consulta')
            }),
            ('Valores', {
                'fields': ('vlr_consulta', 'vlr_pago')
            }),
            ('Status', {
                'fields': ('is_realizado', 'is_pago')
            }),
        ]
        
        # Adiciona datas do sistema apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    date_hierarchy = 'dat_consulta'
    list_per_page = 30
    
    def paciente_nome(self, obj):
        if obj and obj.fk_paciente:
            return obj.fk_paciente.nome
        return '-'
    paciente_nome.short_description = 'Paciente'
    paciente_nome.admin_order_field = 'fk_paciente__nome'
    
    def terapeuta_nome(self, obj):
        if obj and obj.fk_terapeuta:
            return obj.fk_terapeuta.nome
        return '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def status_realizacao(self, obj):
        if obj.is_realizado is None:
            return format_html('<span style="color:gray;font-weight:bold;">? Indefinido</span>')
        elif obj.is_realizado:
            return format_html('<span style="color:green;font-weight:bold;">✓ Realizada</span>')
        else:
            return format_html('<span style="color:red;font-weight:bold;">✗ Não Realizada</span>')
    status_realizacao.short_description = 'Realização'
    
    def status_pagamento(self, obj):
        if obj.is_pago is None:
            return format_html('<span style="color:gray;font-weight:bold;">? Indefinido</span>')
        elif obj.is_pago:
            return format_html('<span style="color:green;font-weight:bold;">✓ Paga</span>')
        else:
            return format_html('<span style="color:red;font-weight:bold;">✗ Não Paga</span>')
    status_pagamento.short_description = 'Pagamento'
    
    def save_model(self, request, obj, form, change):
        # Garantir que consultas não realizadas não estejam marcadas como pagas
        if obj.is_realizado is False:
            obj.is_pago = False
            obj.vlr_pago = None
        super().save_model(request, obj, form, change)
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


class DashboardAdmin(admin.AdminSite):
    site_header = 'ALLOS Consultório - Administração'
    site_title = 'ALLOS Admin'
    index_title = 'Painel Administrativo'


class FirstkissDataFilter(admin.SimpleListFilter):
    title = 'Período'
    parameter_name = 'periodo'

    def lookups(self, request, model_admin):
        return (
            ('hoje', 'Hoje'),
            ('semana', 'Esta Semana'),
            ('mes', 'Este Mês'),
        )

    def queryset(self, request, queryset):
        hoje = timezone.now().date()
        
        if self.value() == 'hoje':
            return queryset.filter(data=hoje)
        if self.value() == 'semana':
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            fim_semana = inicio_semana + timedelta(days=6)
            return queryset.filter(data__range=[inicio_semana, fim_semana])
        if self.value() == 'mes':
            inicio_mes = hoje.replace(day=1)
            if hoje.month == 12:
                fim_mes = hoje.replace(year=hoje.year + 1, month=1, day=1) - timedelta(days=1)
            else:
                fim_mes = hoje.replace(month=hoje.month + 1, day=1) - timedelta(days=1)
            return queryset.filter(data__range=[inicio_mes, fim_mes])


@admin.register(Firstkiss)
class FirstkissAdmin(admin.ModelAdmin):
    list_display = ('dat_consulta', 'paciente_nome', 'terapeuta_nome', 'consentimento_paciente', 'continuar_mesmo_terapeuta', 'created_at')
    list_filter = (FirstkissDataFilter, 'fk_terapeuta', 'fk_paciente', 'consentimento_paciente', 'continuar_mesmo_terapeuta')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente', 'dat_consulta')
            }),
            ('Consentimento', {
                'fields': ('consentimento_paciente',)
            }),
            ('Avaliação de Bem-estar (1-10)', {
                'fields': ('individual', 'interpessoal', 'social', 'geral'),
                'classes': ('wide',)
            }),
            ('Avaliação da Terapia (1-10)', {
                'fields': ('acolhimento', 'abordagem', 'expectativa'),
                'classes': ('wide',)
            }),
            ('Continuidade', {
                'fields': ('continuar_mesmo_terapeuta',)
            }),
        ]
        
        # Adiciona datas do sistema apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    date_hierarchy = 'dat_consulta'
    list_per_page = 30
    
    def paciente_nome(self, obj):
        if obj and obj.fk_paciente:
            return obj.fk_paciente.nome
        return '-'
    paciente_nome.short_description = 'Paciente'
    paciente_nome.admin_order_field = 'fk_paciente__nome'
    
    def terapeuta_nome(self, obj):
        if obj and obj.fk_terapeuta:
            return obj.fk_terapeuta.nome
        return '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


@admin.register(Lastkiss)
class LastkissAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'terapeuta_nome', 'consentimento_paciente', 'terapia_outro_terapeuta', 'recomendaria_outros', 'created_at')
    list_filter = ('fk_terapeuta', 'fk_paciente', 'consentimento_paciente', 'terapia_outro_terapeuta', 'recomendaria_outros')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente')
            }),
            ('Consentimento', {
                'fields': ('consentimento_paciente',)
            }),
            ('Avaliação de Bem-estar (1-10)', {
                'fields': ('individual', 'interpessoal', 'social', 'geral'),
                'classes': ('wide',)
            }),
            ('Avaliação da Terapia (1-10)', {
                'fields': ('acolhimento', 'abordagem', 'expectativa'),
                'classes': ('wide',)
            }),
            ('Avaliação Final', {
                'fields': ('terapia_outro_terapeuta', 'recomendaria_outros')
            }),
        ]
        
        # Adiciona datas do sistema apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets
    
    list_per_page = 30
    
    def paciente_nome(self, obj):
        if obj and obj.fk_paciente:
            return obj.fk_paciente.nome
        return '-'
    paciente_nome.short_description = 'Paciente'
    paciente_nome.admin_order_field = 'fk_paciente__nome'
    
    def terapeuta_nome(self, obj):
        if obj and obj.fk_terapeuta:
            return obj.fk_terapeuta.nome
        return '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura


@admin.register(Altadesistencia)
class AltadesistenciaAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'terapeuta_nome', 'dat_sessao', 'cancelador', 'created_at')
    list_filter = ('fk_terapeuta', 'fk_paciente', 'cancelador', 'dat_sessao')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome', 'motivo_cancel')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente')
            }),
            ('Detalhes da Sessão', {
                'fields': ('dat_sessao', 'cancelador', 'motivo_cancel')
            }),
        ]
        
        # Adiciona datas do sistema apenas no modo de edição
        if obj:
            fieldsets.append(
                ('Datas do Sistema', {
                    'fields': ('created_at', 'updated_at'),
                    'classes': ('collapse',)
                })
            )
        
        return fieldsets

    list_per_page = 30
    date_hierarchy = 'dat_sessao'
    
    def paciente_nome(self, obj):
        if obj and obj.fk_paciente:
            return obj.fk_paciente.nome
        return '-'
    paciente_nome.short_description = 'Paciente'
    paciente_nome.admin_order_field = 'fk_paciente__nome'
    
    def terapeuta_nome(self, obj):
        if obj and obj.fk_terapeuta:
            return obj.fk_terapeuta.nome
        return '-'
    terapeuta_nome.short_description = 'Terapeuta'
    terapeuta_nome.admin_order_field = 'fk_terapeuta__nome'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Em modo de edição
            return self.readonly_fields
        return ()  # Em modo de criação, nenhum campo somente-leitura