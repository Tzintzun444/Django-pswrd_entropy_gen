from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.http import Http404
from .models import CustomUser, UserNotVerified
from .forms import UserRegistrationForm, CustomLoginForm, VerificationEmailForm, UserSettingsForm
from django.views.generic import TemplateView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.decorators import login_required


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
        # Guardar usuario sin commit para manejar la contraseña
        user = form.save(commit=False)

        # Manejar cambio de contraseña
        new_password = form.cleaned_data.get('password')
        if new_password:
            user.set_password(new_password)

        # Guardar todos los cambios
        user.save()

        # Mantener la sesión activa
        update_session_auth_hash(self.request, user)

        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'instance' not in kwargs:
            kwargs['instance'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        is_linked = SocialAccount.objects.filter(user=self.request.user, provider='google').exists()

        if self.request.user.has_usable_password():
            context['has_password'] = True

        else:
            context['has_password'] = False

        context['linked_google_account'] = is_linked

        return context


class SignUpUserView(CreateView):

    model = UserNotVerified
    form_class = UserRegistrationForm
    template_name = 'registrate_client.html'
    success_url = reverse_lazy('verify_email')

    def form_valid(self, form):

        verification = form.save()
        self.request.session['verification_email'] = form.instance.email
        send_mail(
            'Email verification',
            f'Your verification code is {verification.code}',
            'pswrdentropygen@gmail.com',
            [verification.email],
            fail_silently=False
        )
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


class VerifyEmailUserView(FormView):

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

            form.add_error('code', _('Invalid code or expired'))
            return self.form_invalid(form)

        role = 'customer'

        if verification.data['is_admin']:
            role = 'admin'

        user = CustomUser(
            username=verification.data['username'],
            first_name=verification.data['first_name'],
            last_name=verification.data['last_name'],
            email=verification.email,
            is_verified=True,
            role=role,
            is_staff=verification.data['is_admin'],
            is_superuser=verification.data['is_admin']
        )
        user.set_password(verification.data['password'])
        user.save()

        verification.delete()
        if 'verification_email' in self.request.session:
            del self.request.session['verification_email']

        user.backend = "django.contrib.auth.backends.ModelBackend"
        login(self.request, user)
        return redirect(self.get_success_url())

    def dispatch(self, request, *args, **kwargs):

        if request.user.is_authenticated and not (request.user.is_superuser or request.user.is_staff):
            return redirect('index')

        return super().dispatch(request, *args, **kwargs)


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

    def get(self, request, *args, **kwargs):

        raise Http404('Page not found')


@login_required
def unlink_oauth_google(request):

    if request.method != 'POST':

        raise Http404('Page not found')

    google_account = SocialAccount.objects.filter(user=request.user, provider='google').first()
    if google_account:
        google_account.delete()

    return redirect('settings')
