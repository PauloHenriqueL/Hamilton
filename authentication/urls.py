from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


#  Urls para pegar json urls tokens
urlpatterns = [
    path('authentication/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
