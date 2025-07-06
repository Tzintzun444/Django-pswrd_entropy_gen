from django.urls import path, include
from django.views.i18n import set_language
from rest_framework.routers import DefaultRouter
from .viewsets import CustomClientViewSet, CustomAdminViewSet, AllUsersViewSet
from .views import *

router = DefaultRouter()
router.register('customers', CustomClientViewSet, basename='customer')
router.register('admins', CustomAdminViewSet, basename='admin')
router.register('all-users', AllUsersViewSet, basename='all-users')

urlpatterns = [
    path('settings/', UserSettingsView.as_view(), name='settings'),
    path('unlink-google/', unlink_oauth_google, name='unlink_google'),
    path('sign-up/', SignUpUserView.as_view(), name='sign_up'),
    path('verify-email/', VerifyEmailUserView.as_view(), name='verify_email'),
    path('login/', CustomLogInView.as_view(), name='login'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),
    path('delete-user/', DeleteUser.as_view(), name='delete_user'),
    path('set_language/', set_language, name='set_language'),
    path('api/', include(router.urls))
]
