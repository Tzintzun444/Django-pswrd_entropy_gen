from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import CustomUser
from .forms import UserRegistrationForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.models import BaseUserManager


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterClientView(CreateView):

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'registrate_client.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        form.instance.role = 'customer'
        form.instance.is_staff = False
        form.instance.is_superuser = False
        return super().form_valid(form)


class RegisterAdminView(UserPassesTestMixin, CreateView):

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'registrate_admin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        form.instance.role = "admin"
        form.instance.is_staff = True
        form.instance.is_superuser = True
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser
