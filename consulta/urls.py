from django.urls import path
from . import views


urlpatterns = [
    path('consulta', views.ConsultaCreateListView.as_view(), name='consulta-list'),
    path('consulta/<int:pk>', views.ConsultaRetrieveUpdateDestoyView.as_view(), name='consulta-update'),
]
