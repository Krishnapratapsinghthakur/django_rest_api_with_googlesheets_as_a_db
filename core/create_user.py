import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Create a new user
try:
    user = User.objects.create_user('krishna', 'krishna@example.com', 'krishna123')
    print(f"✅ User created successfully!")
    print(f"   Username: krishna")
    print(f"   Password: krishna123")
except Exception as e:
    if 'UNIQUE constraint' in str(e):
        print("User 'krishna' already exists!")
    else:
        print(f"Error: {e}")
