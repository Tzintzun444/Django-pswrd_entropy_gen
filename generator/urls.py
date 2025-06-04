from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PasswordViewSet, AllPasswordsViewSet
from .views import *

router = DefaultRouter()
router.register('passwords', PasswordViewSet, basename='password')
router.register('all-passwords', AllPasswordsViewSet, basename='all_passwords')

urlpatterns = [
    path('generate-passwords/', CreatePasswordView.as_view(), name='generator'),
    path('my-passwords/', PasswordListView.as_view(), name='my_passwords'),
    path('delete-password/<int:pk>/', PasswordDeleteView.as_view(), name='delete_password'),
    path('save-password/', SavePasswordView.as_view(), name='save_password'),
    path('api/', include(router.urls), )
]
