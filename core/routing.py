# mysite/routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat3.routing
import users.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            chat3.routing.websocket_urlpatterns + users.routing.websocket_urlpatterns
        )
    ),
})

# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat3.routing
# import users.routing

# application = ProtocolTypeRouter({
#     'websocket': URLRouter(
#         chat3.routing.websocket_urlpatterns + users.routing.websocket_urlpatterns
#     ),
# })




# mysite/routing.py
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat3.routing
# import users.routing

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': AuthMiddlewareStack(
#         URLRouter(
#             chat3.routing.websocket_urlpatterns,
#             users.routing.websocket_urlpatterns,
            
#         )
#     ),
# })

# from django.core.handlers.exception import ServerErrorsMiddleware
# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# import chat3.routing
# # import users.routing

# application = ProtocolTypeRouter({
#     # (http->django views is added by default)
#     'websocket': ServerErrorsMiddleware(
#         AuthMiddlewareStack(
#             URLRouter(
#                 chat3.routing.websocket_urlpatterns,
#                 # users.routing.websocket_urlpatterns,
#             )
#         )
#     ),
# })

