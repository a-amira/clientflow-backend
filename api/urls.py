from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (
    CompanyViewSet, ClientViewSet, ProjectViewSet, MilestoneViewSet,
    DocumentViewSet, EventViewSet, PaymentViewSet, NotificationViewSet, ActivityViewSet
)

router = DefaultRouter()
router.register(r'companies', CompanyViewSet, basename='company')
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'milestones', MilestoneViewSet, basename='milestone')
router.register(r'documents', DocumentViewSet, basename='document')
router.register(r'events', EventViewSet, basename='event')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'notifications', NotificationViewSet, basename='notification')
router.register(r'activities', ActivityViewSet, basename='activity')

urlpatterns = [
    path('', include(router.urls)),
]