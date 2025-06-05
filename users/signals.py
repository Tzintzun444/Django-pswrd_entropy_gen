from allauth.socialaccount.signals import pre_social_login
from django.dispatch import receiver
from .models import CustomUser


@receiver(pre_social_login)
def link_to_existing_user(sender, request, sociallogin, **kwargs):

    email = sociallogin.account.extra_data.get('email')

    if email:
        try:

            user = CustomUser.objects.get(email=email)
            sociallogin.connect(request, user)

        except CustomUser.DoesNotExist:

            username = sociallogin.account.extra_data.get('username', email.split('@')[0])
            first_name = sociallogin.account.extra_data.get('given_name', '')
            last_name = sociallogin.account.extra_data.get('family_name', '')

            user = CustomUser.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                password=None
            )
            sociallogin.connect(request, user)
