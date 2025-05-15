from django.urls import path
from .views import *

urlpatterns = [
    path('generate-passwords/', CreatePasswordView.as_view(), name='generator'),
]
