from django.urls import path
from . import views


urlpatterns = [
    path('clinica', views.ClinicaCreateListView.as_view(), name='clinica-list'),
    path('clinica/<int:pk>', views.ClinicaRetrieveUpdateDestoyView.as_view(), name='clinica-update'),
]
