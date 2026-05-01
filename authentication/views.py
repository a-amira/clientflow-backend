from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer, UserSerializer

# 1. VUE DE LOGIN (Automatisée avec SimpleJWT)
# Elle utilise ton CustomTokenObtainPairSerializer pour renvoyer tokens + infos user
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 2. VUE D'INSCRIPTION (Register)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # On renvoie un message ET les infos de l'utilisateur créé
        return Response({
            'message': 'Utilisateur créé avec succès',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 3. VUE DE PROFIL (Test de connexion)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    # On utilise le UserSerializer pour renvoyer les données proprement
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

