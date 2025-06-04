from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import PasswordViewSet
from .views import *

router = DefaultRouter()
router.register('passwords', PasswordViewSet, basename='password')
urlpatterns = [
    path('generate-passwords/', CreatePasswordView.as_view(), name='generator'),
    path('my-passwords/', PasswordListView.as_view(), name='my_passwords'),
    path('delete-password/<int:pk>/', PasswordDeleteView.as_view(), name='delete_password'),
    path('save-password/', SavePasswordView.as_view(), name='save_password'),
    path('api/', include(router.urls), )
]
