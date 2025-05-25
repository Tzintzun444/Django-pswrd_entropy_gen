from xml.etree.ElementInclude import include

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import CustomClientViewSet, CustomAdminViewSet
from .views import *

router = DefaultRouter()
router.register('customers', CustomClientViewSet, basename='customer')
router.register('admins', CustomAdminViewSet)

urlpatterns = [
    path('register-customer/', RegisterClientView.as_view(), name='register_customer'),
    path('register-admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('verify-email/', VerifyEmailCustomerView.as_view(), name='verify_email_customer'),
    path('verify-email-admin/', VerifyEmailAdminView.as_view(), name='verify_email_admin'),
    path('login/', CustomLogInView.as_view(), name='login'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),
    path('api/', include(router.urls))
]
