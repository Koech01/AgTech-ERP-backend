from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Creates a default Admin user'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(email='admin@example.com').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='AdminPass123!',
                role=User.Role.ADMIN
            )
            self.stdout.write(self.style.SUCCESS('Admin user created.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))