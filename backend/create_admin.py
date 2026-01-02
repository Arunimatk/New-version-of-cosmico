import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cosmico_backend.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

try:
    if not User.objects.filter(username='arunima').exists():
        User.objects.create_superuser('arunima', 'arunima@example.com', 'password994620')
        print("Successfully created superuser 'arunima'")
    else:
        print("Superuser 'arunima' already exists")
        # Optional: reset password if it exists just to be sure?
        u = User.objects.get(username='arunima')
        u.set_password('password994620')
        u.save()
        print("Updated password for 'arunima'")

except Exception as e:
    print(f"Error: {e}")
