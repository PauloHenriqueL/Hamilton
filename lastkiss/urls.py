from django.urls import path
from . import views


urlpatterns = [
    path('lastkiss', views.RegistroCreateListView.as_view(), name='lastkiss-list'),
    path('lastkiss/<int:pk>', views.RegistroRetrieveUpdateDestoyView.as_view(), name='lastkiss-update'),
]
