from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import UserNotVerified


class Command(BaseCommand):

    help = 'Deletes unverified users whose code has expired'

    def handle(self, *args, **kwargs):

        now = timezone.now()
        expired = UserNotVerified.objects.filter(expires_at__lt=now)
        count = expired.count()
        expired.delete()
        self.stdout.write(f"Expired users deleted: {count}")
