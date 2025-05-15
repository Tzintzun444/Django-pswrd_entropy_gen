from django.urls import path
from .views import *

urlpatterns = [
    path('generate-passwords/', CreatePasswordView.as_view(), name='generator'),
    path('my-passwords/', PasswordListView.as_view(), name='my_passwords')
]
