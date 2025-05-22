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
    list_display = (
        'nome', 'telefone', 'email', 'vlr_sessao_formatado', 
        'status_ativo', 'total_consultas', 'consultas_realizadas',
        'data_ultima_consulta', 'data_primeira_consulta', 'created_at'
    )

    search_fields = ('nome', 'email', 'telefone', 'nome_contato_apoio')
    readonly_fields = (
        'created_at', 'updated_at', 'total_consultas', 'consultas_realizadas',
        'data_ultima_consulta', 'data_primeira_consulta', 'valor_total_pago',
        'valor_total_pendente', 'media_valor_consulta'
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Pessoais', {
                'fields': ('nome', 'email', 'telefone', 'dat_nascimento')
            }),
            ('Contato de Apoio', {
                'fields': ('nome_contato_apoio', 'parentesco_contato_apoio', 'contato_apoio'),
                'classes': ('collapse',)
            }),
            ('Informações de Cadastro', {
                'fields': ('fk_clinica', 'fk_captacao', 'vlr_sessao', 'is_active')
            }),
        ]
        
        if obj:
            fieldsets.append(
                ('Estatísticas Detalhadas', {
                    'fields': (
                        'total_consultas', 'consultas_realizadas', 
                        'data_primeira_consulta', 'data_ultima_consulta',
                        'valor_total_pago', 'valor_total_pendente', 'media_valor_consulta'
                    ),
                    'classes': ('collapse',)
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
    list_per_page = 25
    actions = ['ativar_pacientes', 'desativar_pacientes']

    def vlr_sessao_formatado(self, obj):
        try:
            return f"R$ {obj.vlr_sessao:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except:
            return "R$ 0,00"
    vlr_sessao_formatado.short_description = 'Valor da Sessão'
    vlr_sessao_formatado.admin_order_field = 'vlr_sessao'

    def status_ativo(self, obj):
        if obj.is_active:
            return format_html('<span style="color:green;font-weight:bold;">✓ Ativo</span>')
        return format_html('<span style="color:red;font-weight:bold;">✗ Inativo</span>')
    status_ativo.short_description = 'Status'
    
    def total_consultas(self, obj):
        if obj and obj.pk:
            return Consulta.objects.filter(fk_paciente=obj).count()
        return 0
    total_consultas.short_description = 'Total Consultas'
    
    def consultas_realizadas(self, obj):
        if obj and obj.pk:
            realizadas = Consulta.objects.filter(fk_paciente=obj, is_realizado=True).count()
            total = Consulta.objects.filter(fk_paciente=obj).count()
            if total > 0:
                percentual = (realizadas / total) * 100
                color = 'green' if percentual >= 80 else 'orange' if percentual >= 60 else 'red'
                return format_html(
                    '<span style="color:{};">{}/{} ({}%)</span>',
                    color, realizadas, total, int(percentual)
                )
            return '0/0'
        return '0/0'
    consultas_realizadas.short_description = 'Realizadas'
    
    def data_ultima_consulta(self, obj):
        if obj and obj.pk:
            ultima = Consulta.objects.filter(fk_paciente=obj).order_by('-dat_consulta').first()
            if ultima and ultima.dat_consulta:
                return ultima.dat_consulta.strftime('%d/%m/%Y')
        return '-'
    data_ultima_consulta.short_description = 'Última Consulta'
    
    def data_primeira_consulta(self, obj):
        if obj and obj.pk:
            primeira = Consulta.objects.filter(fk_paciente=obj).order_by('dat_consulta').first()
            if primeira and primeira.dat_consulta:
                return primeira.dat_consulta.strftime('%d/%m/%Y')
        return '-'
    data_primeira_consulta.short_description = 'Primeira Consulta'
    
    def valor_total_pago(self, obj):
        if obj and obj.pk:
            total = Consulta.objects.filter(
                fk_paciente=obj, is_pago=True
            ).aggregate(Sum('vlr_pago'))['vlr_pago__sum'] or 0
            return f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    valor_total_pago.short_description = 'Total Pago'
    
    def valor_total_pendente(self, obj):
        if obj and obj.pk:
            total = Consulta.objects.filter(
                fk_paciente=obj, is_realizado=True, is_pago=False
            ).aggregate(Sum('vlr_consulta'))['vlr_consulta__sum'] or 0
            return f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    valor_total_pendente.short_description = 'Total Pendente'
    
    def media_valor_consulta(self, obj):
        if obj and obj.pk:
            media = Consulta.objects.filter(fk_paciente=obj).aggregate(
                Avg('vlr_consulta')
            )['vlr_consulta__avg'] or 0
            return f"R$ {media:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    media_valor_consulta.short_description = 'Média por Consulta'

    # Actions personalizadas
    def ativar_pacientes(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} paciente(s) ativado(s) com sucesso.')
    ativar_pacientes.short_description = "Ativar pacientes selecionados"

    def desativar_pacientes(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} paciente(s) desativado(s) com sucesso.')
    desativar_pacientes.short_description = "Desativar pacientes selecionados"
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ('created_at', 'updated_at')


@admin.register(Terapeuta)
class TerapeutaAdmin(admin.ModelAdmin):
    list_display = (
        'nome', 'email', 'telefone', 'abordagem_nome', 'clinica_nome', 
        'status_ativo', 'total_pacientes', 'total_consultas', 'taxa_realizacao_formatada',
        'receita_total', 'created_at'
    )
    list_filter = (
        IsActiveFilter, 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 
        'fk_modalidade', 'sexo', 'fk_decano', 'created_at'
    )
    search_fields = ('nome', 'email', 'telefone', 'faculdade')
    readonly_fields = (
        'created_at', 'updated_at', 'total_pacientes', 'total_consultas', 
        'taxa_realizacao', 'receita_total', 'receita_pendente', 
        'media_consultas_por_paciente', 'paciente_mais_frequente'
    )
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Pessoais', {
                'fields': ('nome', 'email', 'telefone', 'dat_nascimento', 'sexo')
            }),
            ('Informações Acadêmicas', {
                'fields': ('faculdade',)
            }),
            ('Informações Profissionais', {
                'fields': ('fk_decano', 'fk_abordagem', 'fk_nucleo', 'fk_clinica', 'fk_modalidade')
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
        ]
        
        if obj:
            fieldsets.append(
                ('Estatísticas Detalhadas', {
                    'fields': (
                        'total_pacientes', 'total_consultas', 'taxa_realizacao',
                        'receita_total', 'receita_pendente', 'media_consultas_por_paciente',
                        'paciente_mais_frequente'
                    ),
                    'classes': ('collapse',)
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
    actions = ['ativar_terapeutas', 'desativar_terapeutas']
    
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
    abordagem_nome.admin_order_field = 'fk_abordagem__abordagem'
    
    def clinica_nome(self, obj):
        if obj and obj.fk_clinica:
            return obj.fk_clinica.clinica
        return '-'
    clinica_nome.short_description = 'Clínica'
    clinica_nome.admin_order_field = 'fk_clinica__clinica'
    
    def total_pacientes(self, obj):
        if obj and obj.pk:
            return Consulta.objects.filter(fk_terapeuta=obj).values('fk_paciente').distinct().count()
        return 0
    total_pacientes.short_description = 'Pacientes'
    
    def total_consultas(self, obj):
        if obj and obj.pk:
            return Consulta.objects.filter(fk_terapeuta=obj).count()
        return 0
    total_consultas.short_description = 'Consultas'
    
    def taxa_realizacao(self, obj):
        if obj and obj.pk:
            consultas = Consulta.objects.filter(fk_terapeuta=obj)
            total = consultas.count()
            realizadas = consultas.filter(is_realizado=True).count()
            if total > 0:
                return (realizadas / total) * 100
        return 0
    taxa_realizacao.short_description = 'Taxa Realização (%)'
    
    def taxa_realizacao_formatada(self, obj):
        taxa = self.taxa_realizacao(obj)
        if taxa > 0:
            color = 'green' if taxa >= 80 else 'orange' if taxa >= 60 else 'red'
            return format_html(
                '<span style="color:{};">{:.1f}%</span>',
                color, taxa
            )
        return "0%"
    taxa_realizacao_formatada.short_description = 'Taxa Real.'
    
    def receita_total(self, obj):
        if obj and obj.pk:
            total = Consulta.objects.filter(
                fk_terapeuta=obj, is_pago=True
            ).aggregate(Sum('vlr_pago'))['vlr_pago__sum'] or 0
            return f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    receita_total.short_description = 'Receita Total'
    
    def receita_pendente(self, obj):
        if obj and obj.pk:
            total = Consulta.objects.filter(
                fk_terapeuta=obj, is_realizado=True, is_pago=False
            ).aggregate(Sum('vlr_consulta'))['vlr_consulta__sum'] or 0
            return f"R$ {total:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return "R$ 0,00"
    receita_pendente.short_description = 'Receita Pendente'
    
    def media_consultas_por_paciente(self, obj):
        if obj and obj.pk:
            total_consultas = Consulta.objects.filter(fk_terapeuta=obj).count()
            total_pacientes = Consulta.objects.filter(fk_terapeuta=obj).values('fk_paciente').distinct().count()
            if total_pacientes > 0:
                return f"{total_consultas / total_pacientes:.1f}"
        return "0"
    media_consultas_por_paciente.short_description = 'Média Cons./Paciente'
    
    def paciente_mais_frequente(self, obj):
        if obj and obj.pk:
            paciente = Consulta.objects.filter(fk_terapeuta=obj).values(
                'fk_paciente__nome'
            ).annotate(
                total=Count('fk_paciente')
            ).order_by('-total').first()
            
            if paciente:
                return f"{paciente['fk_paciente__nome']} ({paciente['total']} consultas)"
        return "-"
    paciente_mais_frequente.short_description = 'Paciente + Frequente'

    # Actions personalizadas
    def ativar_terapeutas(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} terapeuta(s) ativado(s) com sucesso.')
    ativar_terapeutas.short_description = "Ativar terapeutas selecionados"

    def desativar_terapeutas(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} terapeuta(s) desativado(s) com sucesso.')
    desativar_terapeutas.short_description = "Desativar terapeutas selecionados"
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields
        return ('created_at', 'updated_at')

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
    list_display = ('dat_consulta', 'paciente_nome', 'terapeuta_nome','created_at')
    list_filter = (FirstkissDataFilter, 'fk_terapeuta', 'fk_paciente')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente', 'dat_consulta')
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


@admin.register(Altadesistencia)
class AltadesistenciaAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'terapeuta_nome','created_at')
    list_filter = ('fk_terapeuta', 'fk_paciente')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente')
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


@admin.register(Lastkiss)
class LastkissAdmin(admin.ModelAdmin):
    list_display = ('paciente_nome', 'terapeuta_nome','created_at')
    list_filter = ('fk_terapeuta', 'fk_paciente')
    search_fields = ('fk_paciente__nome', 'fk_terapeuta__nome')
    readonly_fields = ('created_at', 'updated_at')
    
    def get_fieldsets(self, request, obj=None):
        fieldsets = [
            ('Informações Básicas', {
                'fields': ('fk_terapeuta', 'fk_paciente')
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
