from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Company, Client, Project, Milestone, Document, Event, Payment, Notification, Activity


# =============================================
# USER SERIALIZER
# =============================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


# =============================================
# COMPANY SERIALIZER
# =============================================

class CompanySerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'owner', 'name', 'slug', 'description', 'email', 'phone', 'address', 'industry', 'is_active', 'created_at', 'updated_at']


# =============================================
# CLIENT SERIALIZER
# =============================================

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'company', 'user', 'first_name', 'last_name', 'email', 'phone', 'company_name', 'address', 'created_at', 'updated_at']


# =============================================
# PROJECT SERIALIZERS
# =============================================

class ProjectListSerializer(serializers.ModelSerializer):
    client_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = ['id', 'company' , 'client' ,'title', 'status', 'progress_percentage', 'quote_amount', 'amount_paid', 'client_name', 'created_at']
    
    def get_client_name(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"


class ProjectDetailSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    company = CompanySerializer(read_only=True)
    remaining_amount = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'company', 'client', 'title', 'description', 'status', 'progress_percentage', 'start_date', 'estimated_completion_date', 'actual_completion_date', 'quote_amount', 'amount_paid', 'remaining_amount', 'created_at', 'updated_at']
    
    def get_remaining_amount(self, obj):
        return obj.remaining_amount


# =============================================
# MILESTONE SERIALIZER
# =============================================

class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ['id', 'project', 'title', 'description', 'order', 'status', 'planned_date', 'actual_date', 'created_at']


# =============================================
# DOCUMENT SERIALIZER
# =============================================

class DocumentSerializer(serializers.ModelSerializer):
    uploaded_by = UserSerializer(read_only=True)

    class Meta:
        model = Document
        fields = ['id', 'project', 'title', 'doc_type', 'file', 'version', 'uploaded_by', 'uploaded_at', 'is_signed']


# =============================================
# EVENT SERIALIZER
# =============================================

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'project', 'title', 'description', 'event_type', 'start_datetime', 'end_datetime', 'location', 'participants', 'created_at']


# =============================================
# PAYMENT SERIALIZER
# =============================================

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'project', 'amount', 'status', 'payment_method', 'stripe_payment_intent_id', 'description', 'due_date', 'created_at', 'updated_at']


# =============================================
# NOTIFICATION SERIALIZER
# =============================================

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'user', 'notification_type', 'title', 'message', 'related_project', 'is_read', 'created_at']


# =============================================
# ACTIVITY SERIALIZER
# =============================================

class ActivitySerializer(serializers.ModelSerializer):
    performed_by = UserSerializer(read_only=True)

    class Meta:
        model = Activity
        fields = ['id', 'project', 'action', 'description', 'performed_by', 'changes', 'created_at']