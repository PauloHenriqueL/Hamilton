from django.urls import path
from . import views


urlpatterns = [
    path('terapeuta', views.TerapeutaCreateListView.as_view(), name='terapeuta-list'),
    path('terapeuta/<int:pk>', views.TerapeutaRetriveUpdateDestroyView.as_view(), name='terapeuta-update'),
]
