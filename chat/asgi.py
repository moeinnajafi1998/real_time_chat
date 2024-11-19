import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat.settings')

# Ensure the application is initialized before importing routing
application = get_asgi_application()

import parse_chat.routing  # Import this after initializing Django

application = ProtocolTypeRouter({
    "http": application,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            parse_chat.routing.websocket_urlpatterns
        )
    ),
})
