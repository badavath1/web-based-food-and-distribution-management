import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_donation_system.settings')
django.setup()

from donations.models import Donation

count = Donation.objects.count()
print('Donation count:', count)
for d in Donation.objects.order_by('-created_at')[:10]:
    print(d.id, d.title, d.donor.username, d.status, d.created_at.isoformat())
