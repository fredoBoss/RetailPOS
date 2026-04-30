from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile


DEMO_USERS = [
    ('superAdmin@example.com', 'superadmin', 'Super Admin', 'superadmin'),
    ('admin@example.com', 'admin', 'Admin', 'admin'),
    ('cashier@example.com', 'cashier', 'Cashier', 'cashier'),
]
DEMO_PASSWORD = 'demo1234'


class Command(BaseCommand):
    help = 'Create demo superadmin, admin, and cashier accounts'

    def handle(self, *args, **kwargs):
        for email, username, display, role in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'first_name': display},
            )
            user.email = email
            user.set_password(DEMO_PASSWORD)
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()

            label = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{label}: {email}  role={role}  password={DEMO_PASSWORD}'))
