from django.urls import path
from .views import *

url_patterns = [
    path('register-client', RegisterClientView.as_view(), name='register_client'),
    path('register-admin', RegisterAdminView.as_view(), name='register-admin')
]