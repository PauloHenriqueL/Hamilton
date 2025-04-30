from django.urls import path
from . import views 


urlpatterns = [
    path('paciente', views.PacienteCreateViewList.as_view(), name='paciente-list'),
    path('paciente/<int:pk>/', views.PacienteRetriveUpdateDestroyView.as_view(), name='paciente-update'),
]
