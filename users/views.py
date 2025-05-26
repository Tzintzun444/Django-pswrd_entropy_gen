from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.utils import timezone
from django.http import Http404
from .models import CustomUser, UserNotVerified
from .forms import UserRegistrationForm, CustomLoginForm, VerificationEmailForm, UserSettingsForm
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'


class UserSettingsView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = 'settings.html'
    form_class = UserSettingsForm
    success_url = reverse_lazy('settings')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        user = form.instance
        username = form.cleaned_data['username']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_password = form.cleaned_data['new_password']

        if username:
            user.username = username
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if new_password:
            user.set_password(new_password)

        user.email = self.request.user.email

        user.save()
        update_session_auth_hash(self.request, user)
        login(self.request, user)
        return super().form_valid(form)


class RegisterClientView(CreateView):

    model = UserNotVerified
    form_class = UserRegistrationForm
    template_name = 'registrate_client.html'
    success_url = reverse_lazy('verify_email_customer')

    def form_valid(self, form):

        verification = form.save()
        self.request.session['verification_email'] = form.instance.email
        send_mail(
            'Email verification',
            f'Your verification code is {verification.code}',
            'alfredotzintzun444@gmail.com',
            [verification.email],
            fail_silently=False
        )

        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class RegisterAdminView(LoginRequiredMixin, UserPassesTestMixin, CreateView):

    model = UserNotVerified
    form_class = UserRegistrationForm
    template_name = 'registrate_admin.html'
    success_url = reverse_lazy('verify_email_admin')

    def form_valid(self, form):
        verification = form.save()
        self.request.session['verification_email'] = form.instance.email
        send_mail(
            'Email verification',
            f'Your verification code is {verification.code}',
            'alfredotzintzun444@gmail.com',
            [verification.email],
            fail_silently=False
        )

        return super().form_valid(form)

    def test_func(self):
        return self.request.user.is_superuser


class VerifyEmailCustomerView(FormView):

    template_name = 'verify_email.html'
    form_class = VerificationEmailForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        user_code = form.cleaned_data['code']
        user_email = self.request.session.get('verification_email')

        try:

            verification = UserNotVerified.objects.get(
                email=user_email,
                code=user_code,
                expires_at__gte=timezone.now()
            )

        except UserNotVerified.DoesNotExist:

            form.add_error('code', 'Invalide code or expired')
            return self.form_invalid(form)
        user = CustomUser(
            username=verification.data['username'],
            first_name=verification.data['first_name'],
            last_name=verification.data['last_name'],
            email=verification.email,
            password=verification.data['password'],
            is_verified=True,
            role='customer'
        )
        user.is_staff = False
        user.is_superuser = False
        user.save()
        verification.delete()
        del self.request.session['verification_email']

        login(self.request, user)
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class VerifyEmailAdminView(LoginRequiredMixin, UserPassesTestMixin, FormView):

    template_name = 'verify_email_admin.html'
    form_class = VerificationEmailForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):

        user_code = form.cleaned_data['code']
        user_email = self.request.session.get('verification_email')

        try:

            verification = UserNotVerified.objects.get(
                email=user_email,
                code=user_code,
                expires_at__gte=timezone.now()
            )

        except UserNotVerified.DoesNotExist:

            form.add_error('code', 'Invalide code or expired')
            return self.form_invalid(form)
        user = CustomUser(
            username=verification.data['username'],
            first_name=verification.data['first_name'],
            last_name=verification.data['last_name'],
            email=verification.email,
            password=verification.data['password'],
            is_verified=True,
            role='customer'
        )
        user.is_staff = True
        user.is_superuser = True
        user.save()
        verification.delete()
        del self.request.session['verification_email']

        login(self.request, user)
        return redirect(self.get_success_url())

    def test_func(self):
        return self.request.user.is_superuser


class CustomLogInView(LoginView):

    template_name = 'login.html'
    form_class = CustomLoginForm
    redirect_authenticated_user = True

    def form_valid(self, form):

        user = form.get_user()
        user.user_status = True
        user.last_login = timezone.now()
        user.save(update_fields=['user_status', 'last_login'])

        return super().form_valid(form)


class CustomLogOutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            request.user.user_status = False
            request.user.save(update_fields=['user_status'])

        return super().dispatch(request, *args, **kwargs)


class DeleteUser(LoginRequiredMixin, DeleteView):

    model = CustomUser
    template_name = 'delete_user.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kargs):

        raise Http404('Page not found')
