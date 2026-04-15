from rest_framework.permissions import BasePermission


class IsCompanyOwner(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est le propriétaire de l'entreprise.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Retourner True si l'utilisateur est le propriétaire de l'entreprise.
        """
        return obj.owner == request.user


class IsCompanyMember(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est membre de l'entreprise.
    """
    
    def has_permission(self, request, view):
        """
        Vérifier que l'utilisateur est authentifié.
        """
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        """
        Vérifier que l'utilisateur est propriétaire de l'entreprise.
        """
        # Pour les projets, clients, milestones, etc.
        if hasattr(obj, 'company'):
            return obj.company.owner == request.user
        # Pour les entreprises
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        return False


class IsProjectOwner(BasePermission):
    """
    Permission pour vérifier que l'utilisateur est propriétaire du projet.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Vérifier que l'utilisateur est propriétaire de l'entreprise du projet.
        """
        return obj.company.owner == request.user


class IsDocumentOwner(BasePermission):
    """
    Permission pour vérifier que l'utilisateur peut accéder au document.
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Vérifier que le document appartient à un projet de l'utilisateur.
        """
        return obj.project.company.owner == request.user


class ReadOnly(BasePermission):
    """
    Permission pour l'accès lecture seule (Activities).
    """
    
    def has_permission(self, request, view):
        """
        Autoriser seulement les méthodes GET, HEAD, OPTIONS.
        """
        return request.method in ['GET', 'HEAD', 'OPTIONS']