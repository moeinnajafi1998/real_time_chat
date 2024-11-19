# your_app/routing.py
from django.urls import path,re_path
from .consumers import *

websocket_urlpatterns = [
    path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
    re_path(r'ws/private_chat/(?P<user1_id>\d+)/(?P<user2_id>\d+)/$', PrivateChatConsumer.as_asgi()),

]
