from django.urls import path
from . import views


urlpatterns = [
    path('prefeidade', views.PrefeidadeCreateListView.as_view(), name='prefeidade-list'),
    path('prefeidade/<int:pk>', views.PrefeidadeRetrieveUpdateDestoyView.as_view(), name='prefeidade-update'),
]
