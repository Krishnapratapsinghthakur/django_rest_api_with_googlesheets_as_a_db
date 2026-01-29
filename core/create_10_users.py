import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

# Define 10 users with different emails
users_data = [
    {'username': 'user1', 'email': 'user1@example.com', 'password': 'pass1234'},
    {'username': 'user2', 'email': 'user2@example.com', 'password': 'pass1234'},
    {'username': 'user3', 'email': 'user3@example.com', 'password': 'pass1234'},
    {'username': 'user4', 'email': 'user4@example.com', 'password': 'pass1234'},
    {'username': 'user5', 'email': 'user5@example.com', 'password': 'pass1234'},
    {'username': 'user6', 'email': 'user6@example.com', 'password': 'pass1234'},
    {'username': 'user7', 'email': 'user7@example.com', 'password': 'pass1234'},
    {'username': 'user8', 'email': 'user8@example.com', 'password': 'pass1234'},
    {'username': 'user9', 'email': 'user9@example.com', 'password': 'pass1234'},
    {'username': 'user10', 'email': 'user10@example.com', 'password': 'pass1234'},
]

print("Creating 10 users...")
print("-" * 50)

created_users = []
for user_data in users_data:
    try:
        # Check if user already exists
        if User.objects.filter(username=user_data['username']).exists():
            user = User.objects.get(username=user_data['username'])
            print(f"⚠️  User '{user_data['username']}' already exists")
        else:
            user = User.objects.create_user(
                username=user_data['username'],
                email=user_data['email'],
                password=user_data['password']
            )
            print(f"✅ Created: {user_data['username']} | {user_data['email']} | {user_data['password']}")
        created_users.append(user)
    except Exception as e:
        print(f"❌ Error creating {user_data['username']}: {e}")

print("-" * 50)
print(f"Total users created/found: {len(created_users)}")
print("\n📋 User Credentials:")
print("-" * 50)
print(f"{'Username':<12} | {'Email':<25} | Password")
print("-" * 50)
for u in users_data:
    print(f"{u['username']:<12} | {u['email']:<25} | {u['password']}")
