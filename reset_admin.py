import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_donation_system.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()
username = 'admin'
password = 'Admin123!'
user, created = User.objects.get_or_create(
    username=username,
    defaults={'email': 'admin@example.com', 'is_staff': True, 'is_superuser': True},
)
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()
print('OK: admin ready; username=admin password=Admin123!')
