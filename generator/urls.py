from django.urls import path
from .views import *

urlpatterns = [
    path('generate-passwords/', CreatePasswordView.as_view(), name='generator'),
    path('my-passwords/', PasswordListView.as_view(), name='my_passwords'),
    path('delete-password/<int:pk>/', PasswordDeleteView.as_view(), name='delete_password'),
    path('save_password/', SavePasswordView.as_view(), name='save_password')
]
