from django.urls import path
from .views import *

urlpatterns = [
    path('register-customer/', RegisterClientView.as_view(), name='register_customer'),
    path('register-admin/', RegisterAdminView.as_view(), name='register_admin'),
    path('login/', CustomLogInView.as_view(), name='login'),
    path('logout/', CustomLogOutView.as_view(), name='logout'),
]
