from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from authentication.views import CustomTokenObtainPairView, register, user_profile

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('user-profile/', user_profile, name='user_profile'),
]