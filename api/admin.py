from django.contrib import admin
from api.models import Company, Client, Project, Milestone, Document, Event, Payment, Notification, Activity


# =============================================
# COMPANY ADMIN
# =============================================

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'industry', 'is_active', 'created_at']
    list_filter = ['industry', 'is_active', 'created_at']
    search_fields = ['name', 'email']
    prepopulated_fields = {'slug': ('name',)}


# =============================================
# CLIENT ADMIN
# =============================================

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['get_full_name', 'email', 'company', 'created_at']
    list_filter = ['company', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    get_full_name.short_description = 'Name'


# =============================================
# PROJECT ADMIN
# =============================================

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'progress_percentage', 'quote_amount', 'amount_paid', 'company', 'client', 'created_at']
    list_filter = ['status', 'company', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']


# =============================================
# MILESTONE ADMIN
# =============================================

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'order', 'status', 'planned_date', 'actual_date']
    list_filter = ['status', 'project', 'planned_date']
    search_fields = ['title', 'project__title']
    ordering = ['project', 'order']


# =============================================
# DOCUMENT ADMIN
# =============================================

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'doc_type', 'project', 'version', 'uploaded_by', 'uploaded_at', 'is_signed']
    list_filter = ['doc_type', 'is_signed', 'uploaded_at']
    search_fields = ['title', 'project__title']
    readonly_fields = ['uploaded_at']


# =============================================
# EVENT ADMIN
# =============================================

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'project', 'start_datetime', 'location']
    list_filter = ['event_type', 'start_datetime']
    search_fields = ['title', 'project__title']
    filter_horizontal = ['participants']


# =============================================
# PAYMENT ADMIN
# =============================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'project', 'amount', 'status', 'payment_method', 'due_date', 'created_at']
    list_filter = ['status', 'payment_method', 'created_at']
    search_fields = ['project__title']
    readonly_fields = ['created_at', 'updated_at']


# =============================================
# NOTIFICATION ADMIN
# =============================================

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['title', 'notification_type', 'user', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'user__username']
    readonly_fields = ['created_at']


# =============================================
# ACTIVITY ADMIN
# =============================================

@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['action', 'project', 'performed_by', 'created_at']
    list_filter = ['action', 'created_at']
    search_fields = ['project__title', 'performed_by__username']
    readonly_fields = ['created_at', 'changes']