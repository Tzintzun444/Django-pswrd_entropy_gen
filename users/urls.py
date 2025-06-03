from xml.etree.ElementInclude import include

from django.urls import path, include
from django.views.i18n import set_language
from rest_framework.routers import DefaultRouter
from .viewsets import CustomClientViewSet, CustomAdminViewSet
from .views import *

router = DefaultRouter()
router.register('customers', CustomClientViewSet, basename='customer')
router.register('admins', CustomAdminViewSet, basename='admin')

urlpatterns = [
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('register-customer/', RegisterClientView.as_view(), name='register_customer'),
    path('register-admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('verify-email/', VerifyEmailCustomerView.as_view(), name='verify_email_customer'),
    path('verify-email-admin/', VerifyEmailAdminView.as_view(), name='verify_email_admin'),
    path('login/', CustomLogInView.as_view(), name='login'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),
    path('delete-user/', DeleteUser.as_view(), name='delete_user'),
    path('set_language/', set_language, name='set_language'),
    path('api/', include(router.urls))
]
