from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from .models import CustomUser
from .forms import UserRegistrationForm, CustomLoginForm
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class RegisterClientView(CreateView):

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'registrate_client.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        user = form.save(commit=False)
        user.role = 'customer'
        user.is_staff = False
        user.is_superuser = False
        user.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        authenticated_user = authenticate(
            request=self.request,
            username=username,
            password=password
        )
        login(self.request, authenticated_user, backend='django.contrib.auth.backends.ModelBackend')

        return redirect('index')

    def dispatch(self, request, *args, **kwargs):
        
        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect('index')
        
        return super().dispatch(request, *args, **kwargs)


class RegisterAdminView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = CustomUser
    form_class = UserRegistrationForm
    template_name = 'registrate_admin.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        user = form.save(commit=False)
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = False
        user.save()

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        authenticated_user = authenticate(
            username=username,
            password=password
        )
        login(self.request, authenticated_user)

        return redirect('index')

    def test_func(self):
        return self.request.user.is_superuser


class CustomLogInView(LoginView):

    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True


class CustomLogOutView(LogoutView):
    pass
