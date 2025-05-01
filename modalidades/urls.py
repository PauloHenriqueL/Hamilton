from django.urls import path
from . import views


urlpatterns = [
    path('modalidades', views.ModalidadeCreateListView.as_view(), name='modalidades-list'),
    path('modalidades/<int:pk>', views.ModalidadeRetrieveUpdateDestoyView.as_view(), name='modalidades-update'),
]
