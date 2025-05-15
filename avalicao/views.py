from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from . import models, forms, serializers


class AvaliacaoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = models.Avaliacao
    template_name = 'avaliacao_list.html'  # Certifique-se de que este arquivo existe
    context_object_name = 'avaliacoes'
    paginate_by = 10
    permission_required = 'avaliacao.view_avaliacao'

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filtros para avaliador e avaliado
        avaliador_id = self.request.GET.get('avaliador')
        avaliado_id = self.request.GET.get('avaliado')

        if avaliador_id:
            queryset = queryset.filter(fk_avaliador__pk=avaliador_id)

        if avaliado_id:
            queryset = queryset.filter(fk_avaliado__pk=avaliado_id)
        
        # Log para debug
        print(f"Total de avaliações encontradas: {queryset.count()}")
        return queryset
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona avaliadores e avaliados ao contexto para os filtros
        context['avaliadores'] = models.Avaliador.objects.all()
        context['avaliados'] = models.Avaliado.objects.all()
        return context


class AvaliacaoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = models.Avaliacao
    template_name = 'avaliacao_create.html'
    form_class = forms.AvaliacaoForm
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.add_avaliacao'


class AvaliacaoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = models.Avaliacao
    template_name = 'avaliacao_detail.html'
    context_object_name = 'avaliacao'  # Adicionado para consistência
    permission_required = 'avaliacao.view_avaliacao'


class AvaliacaoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = models.Avaliacao
    template_name = 'avaliacao_update.html'
    form_class = forms.AvaliacaoForm
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.change_avaliacao'


class AvaliacaoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = models.Avaliacao
    template_name = 'avaliacao_delete.html'
    success_url = reverse_lazy('avaliacao-list')
    permission_required = 'avaliacao.delete_avaliacao'


# API Views corrigidas
class AvaliacaoCreateListAPIView(generics.ListCreateAPIView):
    queryset = models.Avaliacao.objects.all()
    serializer_class = serializers.AvaliacaoSerializer
    
    def get(self, request, *args, **kwargs):
        """
        Sobrescreve o método GET para verificar e retornar todas as avaliações
        """
        queryset = self.get_queryset()
        print(f"API - Total de avaliações encontradas: {queryset.count()}")
        
        # Se queryset estiver vazio, ainda retornará uma lista vazia
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        """
        Sobrescreve o método POST para adicionar validações extras se necessário
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AvaliacaoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Avaliacao.objects.all()
    serializer_class = serializers.AvaliacaoSerializer