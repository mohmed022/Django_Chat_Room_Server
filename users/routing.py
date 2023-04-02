# # users/routing.py

# from django.urls import re_path

# from users.consumers import OnlineUsersConsumer
# from django.urls import path

# websocket_urlpatterns = [
#    re_path(r'ws/users/online/$', OnlineUsersConsumer.as_asgi()),

# ]


# from django.urls import re_path
# from .consumers import OnlineUsersConsumer

# websocket_urlpatterns = [
#     re_path(r'ws/user/(?P<user_online>\w+)/$', OnlineUsersConsumer.as_asgi()),
# ]



# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/user/(?P<room_name>\w+)/$', consumers.OnlineUsersConsumer.as_asgi()),
# ]




# from django.urls import re_path

# from . import consumers

# websocket_urlpatterns = [
#     re_path(r'ws/user/$', consumers.OnlineUsersConsumer.as_asgi()),
# ]


from django.urls import path

from . import consumers 

websocket_urlpatterns = [
    path('ws/user/', consumers.Mytest.as_asgi()),
]
