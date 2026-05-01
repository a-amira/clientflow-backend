from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# --- 1. SERIALIZER POUR L'INSCRIPTION (Register) ---
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        # On inclut first_name et last_name pour que la base Neon soit bien remplie
        fields = ['username', 'email', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, attrs):
        # Vérification de sécurité : les deux mots de passe doivent être identiques
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': "Les mots de passe ne correspondent pas."})
        
        # Vérification si l'email existe déjà (important pour éviter les doublons)
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({'email': "Cet email est déjà utilisé."})
            
        return attrs

    def create(self, validated_data):
        # On retire password2 pour ne pas l'envoyer à la base de données
        validated_data.pop('password2')
        # create_user crypte automatiquement le mot de passe avant l'envoi vers Neon
        user = User.objects.create_user(**validated_data)
        return user

# --- 2. SERIALIZER POUR LE LOGIN (JWT) ---
# Ce serializer gère l'authentification SANS avoir besoin d'importer 'authenticate' manuellement
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # On ajoute le username dans le contenu du token lui-même
        token['username'] = user.username
        return token

    def validate(self, attrs):
        # SimpleJWT vérifie ici les identifiants en coulisses
        data = super().validate(attrs)
        
        # ON AJOUTE L'OBJET USER POUR LE FRONTEND
        # C'est ce qui permet à Hafsa de rediriger et d'afficher le profil
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        }
        return data

# --- 3. SERIALIZER POUR RÉCUPÉRER UN UTILISATEUR (User Details) ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')