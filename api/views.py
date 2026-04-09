from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

from api.models import Company, Client, Project, Milestone, Document, Event, Payment, Notification, Activity
from api.serializers import (
    CompanySerializer, ClientSerializer, ProjectListSerializer, ProjectDetailSerializer,
    MilestoneSerializer, DocumentSerializer, EventSerializer, PaymentSerializer,
    NotificationSerializer, ActivitySerializer
)


# =============================================
# COMPANY VIEWSET
# =============================================

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name', 'email']
    ordering_fields = ['created_at', 'name']

    def get_queryset(self):
        return Company.objects.filter(owner=self.request.user)


# =============================================
# CLIENT VIEWSET
# =============================================

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['first_name', 'last_name', 'email']
    ordering_fields = ['created_at', 'last_name']

    def get_queryset(self):
        return Client.objects.filter(company__owner=self.request.user)


# =============================================
# PROJECT VIEWSET
# =============================================

class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'company']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        return Project.objects.filter(company__owner=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectListSerializer

    @action(detail=True, methods=['patch'])
    def update_progress(self, request, pk=None):
        project = self.get_object()
        progress = request.data.get('progress_percentage')
        if progress is not None:
            project.progress_percentage = progress
            project.save()
            return Response({'status': 'progress updated'})
        return Response({'error': 'progress_percentage required'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        project = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Project.STATUS_CHOICES):
            project.status = new_status
            project.save()
            return Response({'status': 'status updated'})
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)


# =============================================
# MILESTONE VIEWSET
# =============================================

class MilestoneViewSet(viewsets.ModelViewSet):
    queryset = Milestone.objects.all()
    serializer_class = MilestoneSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'status']
    ordering_fields = ['order', 'planned_date']

    def get_queryset(self):
        return Milestone.objects.filter(project__company__owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def change_status(self, request, pk=None):
        milestone = self.get_object()
        new_status = request.data.get('status')
        if new_status in dict(Milestone.STATUS_CHOICES):
            milestone.status = new_status
            milestone.save()
            return Response({'status': 'milestone status updated'})
        return Response({'error': 'invalid status'}, status=status.HTTP_400_BAD_REQUEST)


# =============================================
# DOCUMENT VIEWSET
# =============================================

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['project', 'doc_type']
    search_fields = ['title']

    def get_queryset(self):
        return Document.objects.filter(project__company__owner=self.request.user)


# =============================================
# EVENT VIEWSET
# =============================================

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['project', 'event_type']
    search_fields = ['title']
    ordering_fields = ['start_datetime']

    def get_queryset(self):
        return Event.objects.filter(project__company__owner=self.request.user)


# =============================================
# PAYMENT VIEWSET
# =============================================

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'status', 'payment_method']
    ordering_fields = ['created_at', 'due_date', 'amount']

    def get_queryset(self):
        return Payment.objects.filter(project__company__owner=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_as_paid(self, request, pk=None):
        payment = self.get_object()
        payment.status = 'completed'
        payment.save()
        return Response({'status': 'payment marked as completed'})


# =============================================
# NOTIFICATION VIEWSET
# =============================================

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['is_read', 'notification_type']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['patch'])
    def mark_all_as_read(self, request):
        Notification.objects.filter(user=self.request.user, is_read=False).update(is_read=True)
        return Response({'status': 'all notifications marked as read'})


# =============================================
# ACTIVITY VIEWSET
# =============================================

class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['project', 'action']
    ordering_fields = ['created_at']

    def get_queryset(self):
        return Activity.objects.filter(project__company__owner=self.request.user)