from django.urls import path
from . import views


urlpatterns = [
    path('registros', views.RegistroCreateListView.as_view(), name='registros-list'),
    path('registros/<int:pk>', views.RegistroRetrieveUpdateDestoyView.as_view(), name='registros-update'),
]
