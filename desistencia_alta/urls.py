from django.urls import path
from . import views


urlpatterns = [
    path('desistencia_alta', views.Desistencia_altaCreateListView.as_view(), name='desistencia_alta-list'),
    path('desistencia_alta/<int:pk>', views.Desistencia_altaRetrieveUpdateDestoyView.as_view(), name='desistencia_alta-update'),
]
