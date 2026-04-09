from django.db import models
from django.contrib.auth.models import User


# =============================================
# 1. COMPANY MODEL
# =============================================

class Company(models.Model):
    INDUSTRY_CHOICES = [
        ('manufacturing', 'Fabrication'),
        ('services', 'Services'),
        ('hybrid', 'Hybride'),
    ]
    
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    industry = models.CharField(max_length=50, choices=INDUSTRY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


# =============================================
# 2. CLIENT MODEL
# =============================================

class Client(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='clients')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    company_name = models.CharField(max_length=255, blank=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        unique_together = ('company', 'email')
        ordering = ['-created_at']


# =============================================
# 3. PROJECT MODEL
# =============================================

class Project(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('quote', 'Devis'),
        ('in_progress', 'En cours'),
        ('completed', 'Complété'),
        ('delivered', 'Livré'),
        ('paid', 'Payé'),
        ('cancelled', 'Annulé'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='projects')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    progress_percentage = models.IntegerField(default=0)
    
    start_date = models.DateField(null=True, blank=True)
    estimated_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    
    quote_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def remaining_amount(self):
        if self.quote_amount:
            return self.quote_amount - self.amount_paid
        return 0

    class Meta:
        ordering = ['-created_at']


# =============================================
# 4. MILESTONE MODEL
# =============================================

class Milestone(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Complété'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    planned_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.project.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ('project', 'order')


# =============================================
# 5. DOCUMENT MODEL
# =============================================

class Document(models.Model):
    TYPE_CHOICES = [
        ('quote', 'Devis'),
        ('invoice', 'Facture'),
        ('contract', 'Contrat'),
        ('delivery', 'Livrable'),
        ('other', 'Autre'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=255)
    doc_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    version = models.PositiveIntegerField(default=1)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} (v{self.version})"

    class Meta:
        ordering = ['-uploaded_at']
        unique_together = ('project', 'doc_type', 'version')
    
# =============================================
# 6. EVENT MODEL
# =============================================

class Event(models.Model):
    EVENT_TYPES = [
        ('meeting', 'Réunion'),
        ('inspection', 'Inspection'),
        ('delivery', 'Livraison'),
        ('payment', 'Paiement'),
        ('other', 'Autre'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='events')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField(User, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['start_datetime']


# =============================================
# 7. PAYMENT MODEL
# =============================================

class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('processing', 'En traitement'),
        ('completed', 'Complété'),
        ('failed', 'Échoué'),
        ('refunded', 'Remboursé'),
    ]
    
    METHOD_CHOICES = [
        ('card', 'Carte bancaire'),
        ('bank_transfer', 'Virement'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, choices=METHOD_CHOICES)
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.amount}€"

    class Meta:
        ordering = ['-created_at']


# =============================================
# 8. NOTIFICATION MODEL
# =============================================

class Notification(models.Model):
    TYPE_CHOICES = [
        ('project_update', 'Mise à jour projet'),
        ('payment_reminder', 'Rappel de paiement'),
        ('new_document', 'Nouveau document'),
        ('event', 'Événement'),
        ('message', 'Message'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    related_project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


# =============================================
# 9. ACTIVITY MODEL
# =============================================

class Activity(models.Model):
    ACTION_CHOICES = [
        ('created', 'Créé'),
        ('updated', 'Mis à jour'),
        ('status_changed', 'Statut changé'),
        ('document_added', 'Document ajouté'),
        ('payment_recorded', 'Paiement enregistré'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    description = models.TextField()
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changes = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.project.title}"

    class Meta:
        ordering = ['-created_at']
