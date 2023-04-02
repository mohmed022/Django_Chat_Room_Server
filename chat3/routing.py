# # chat/routing.py
# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer),
# ]

# chat/routing.py

from django.urls import re_path

from .consumers import ChatConsumer
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
]



# from django.urls import re_path
# from chat3.consumers import ChatConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
# ]



# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from django.urls import path
# from .consumers import ChatConsumer
# websocket_urlpatterns = [
#     path('ws/chat/<str:room_name>/', ChatConsumer.as_asgi()),
# ]

# application = ProtocolTypeRouter({
#     "websocket": AuthMiddlewareStack(
#         URLRouter(
#             websocket_urlpatterns
#         )
#     ),
# })
