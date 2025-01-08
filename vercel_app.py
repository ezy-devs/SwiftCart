import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SwiftCart.settings')
app = get_wsgi_application()  # 'app' is the entry point Vercel expects
