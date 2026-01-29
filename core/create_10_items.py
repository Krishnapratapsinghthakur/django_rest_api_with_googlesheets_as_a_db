import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from myapi.google_sheets import sheets_service

# Define 10 items, one for each user
items_data = [
    {'name': 'Laptop Dell XPS', 'description': 'High-performance ultrabook', 'email': 'user1@example.com'},
    {'name': 'iPhone 15 Pro', 'description': 'Latest Apple smartphone', 'email': 'user2@example.com'},
    {'name': 'Sony Headphones', 'description': 'Noise-canceling wireless', 'email': 'user3@example.com'},
    {'name': 'Samsung TV 55"', 'description': 'Smart OLED television', 'email': 'user4@example.com'},
    {'name': 'iPad Pro 12.9', 'description': 'M2 chip tablet', 'email': 'user5@example.com'},
    {'name': 'Nintendo Switch', 'description': 'Gaming console hybrid', 'email': 'user6@example.com'},
    {'name': 'Canon Camera', 'description': 'Professional DSLR EOS R5', 'email': 'user7@example.com'},
    {'name': 'MacBook Pro M3', 'description': '14-inch laptop', 'email': 'user8@example.com'},
    {'name': 'Bose Speaker', 'description': 'Portable Bluetooth speaker', 'email': 'user9@example.com'},
    {'name': 'PS5 Console', 'description': 'Next-gen gaming system', 'email': 'user10@example.com'},
]

print("Adding email column header and 10 items to Google Sheet...")
print("-" * 60)

# First, ensure email column exists
try:
    sheets_service.ensure_email_column()
    print("✅ Email column header added/verified")
except Exception as e:
    print(f"⚠️  Email column: {e}")

# Add items
for item in items_data:
    try:
        created = sheets_service.create_row(item, user_email=item['email'])
        print(f"✅ Added: ID {created['id']} | {item['name']} | {item['email']}")
    except Exception as e:
        print(f"❌ Error adding {item['name']}: {e}")

print("-" * 60)
print("Done! Check your Google Sheet for the new data.")
print("\n📊 Items Summary:")
print("-" * 60)
print(f"{'ID':<4} | {'Name':<20} | {'Email':<25}")
print("-" * 60)
for i, item in enumerate(items_data, 1):
    print(f"{i:<4} | {item['name']:<20} | {item['email']:<25}")
