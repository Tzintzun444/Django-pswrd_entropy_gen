from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import get_user_model, login
import re


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed.
        """
        user = sociallogin.user
        if user.id:  # Si el usuario ya existe, no necesitamos hacer nada
            return

        # Verificar si ya existe un usuario con este email
        if user.email:

            User = get_user_model()

            try:

                existing_user = User.objects.get(email=user.email)

                # Conectar la cuenta social al usuario existente
                sociallogin.connect(request, existing_user)
                login(request, existing_user, backend="django.contrib.auth.backends.ModelBackend")

                # Aquí puedes personalizar el mensaje o redirección
                return HttpResponseRedirect(reverse('index'))
            except User.DoesNotExist:
                pass

    def populate_user(self, request, sociallogin, data):
        """
        Popula la instancia de usuario con los datos del proveedor social.
        """
        user = super().populate_user(request, sociallogin, data)

        # Extraer username del email (parte antes del @)
        if user.email:
            username = user.email.split('@')[0]

            # Limpiar el username de caracteres no permitidos
            username = re.sub(r'[^a-zA-Z0-9_\.]', '', username)

            # Verificar si el username ya existe
            from django.contrib.auth import get_user_model
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                # Si existe, usar el email completo como username
                username = user.email

            user.username = username

        extra_data = sociallogin.account.extra_data
        if not user.first_name and 'given_name' in extra_data:
            user.first_name = extra_data.get('given_name', '')
        if not user.last_name and 'family_name' in extra_data:
            user.last_name = extra_data.get('family_name', '')

        return user
