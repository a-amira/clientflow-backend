from rest_framework.exceptions import APIException
from rest_framework import status
class CompanyNotFound(APIException):
    """
    Exception levée quand une entreprise n'existe pas.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Company not found.'
    default_code = 'company_not_found'

class ClientNotFound(APIException):
    """
    Exception levée quand un client n'existe pas.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Client not found.'
    default_code = 'client_not_found'
class ProjectNotFound(APIException):
    """
    Exception levée quand un projet n'existe pas.
    """
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Project not found.'
    default_code = 'project_not_found'
class InvalidProjectStatus(APIException):
    """
    Exception levée quand le statut du projet est invalide.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid project status.'
    default_code = 'invalid_project_status'

class PaymentAlreadyProcessed(APIException):
    """
    Exception levée quand on essaie de traiter un paiement déjà traité.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Payment has already been processed.'
    default_code = 'payment_already_processed'
class InsufficientPermission(APIException):
    """
    Exception levée quand l'utilisateur n'a pas les permissions suffisantes.
    """
    status_code = status.HTTP_403_FORBIDDEN
    default_detail = 'You do not have permission to perform this action.'
    default_code = 'insufficient_permission'

class DocumentUploadError(APIException):
    """
    Exception levée quand il y a une erreur lors du téléchargement d'un document.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Error uploading document.'
    default_code = 'document_upload_error'

class InvalidAmountError(APIException):
    """
    Exception levée quand le montant est invalide.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Invalid amount.'
    default_code = 'invalid_amount'
class QuotaExceededError(APIException):
    """
    Exception levée quand la limite est dépassée.
    """
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_detail = 'Quota exceeded.'
    default_code = 'quota_exceeded'