
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

USERNAME = 'admin'
PASSWORD = 'CosmicoAdmin2025!'
EMAIL = 'admin@cosmico.com'

try:
    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
        print(f"Successfully created superuser '{USERNAME}' with password '{PASSWORD}'")
    else:
        print(f"Superuser '{USERNAME}' already exists. Resetting password.")
        u = User.objects.get(username=USERNAME)
        u.set_password(PASSWORD)
        u.save()
        print(f"Successfully updated password for '{USERNAME}' to '{PASSWORD}'")

except Exception as e:
    print(f"Error: {e}")
