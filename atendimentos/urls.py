from django.urls import path
from . import views


urlpatterns = [
    path('atendimento', views.AtendimentoCreateListView.as_view(), name='atendimento-list'),
    path('atendimento/<int:pk>', views.AtendimentoRetrieveUpdateDestoyView.as_view(), name='atendimento-update'),
]
