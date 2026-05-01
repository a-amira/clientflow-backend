from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView, register, user_profile

urlpatterns = [
    # C'est cette route que Hafsa doit utiliser pour le Login
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Utile pour renouveler le token sans avoir à se reconnecter
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Route pour la création de compte
    path('register/', register, name='register'),
    
    # Route pour récupérer les infos de l'utilisateur connecté
    path('user-profile/', user_profile, name='user_profile'),
]