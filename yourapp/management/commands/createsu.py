import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create superuser automatically"

    def handle(self, *args, **options):
        User = get_user_model()

        username = os.getenv("shim")
        email = os.getenv("sh.s.alsuraihi@gmail.com")
        password = os.getenv("098098")

        if not username or not password:
            self.stdout.write(self.style.ERROR("Missing environment variables"))
            return

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Superuser created successfully"))
        else:
            self.stdout.write("Superuser already exists")