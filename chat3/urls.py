



from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RoomView , ChatList , RoomFulterSerializer , ChatView ,NotificationViewSet

app_name = 'chat3'

router = DefaultRouter()
urlpatterns = [
    # path('chat/<int:room_id>/', ChatList.as_view(), name='chat-list'),
    # path('ChatView/<int:room_id>/', ChatList.as_view(), name='chat_messages'),
    # path('user_rooms/', UserRooms.as_view(), name='user-rooms'),
    # path('addmessage/', add_message, name='add_message'),
    # path('Notifications/<int:room_id>/delete/', NotificationViewSet.as_view({'delete': 'delete'}), name='notification-delete')
    path('Notifications/<int:room_id>/update/', NotificationViewSet.as_view({'put': 'update'}), name='notification-update')



]
router.register('chat', ChatView, basename='ChatView')
router.register('room', RoomView, basename='RoomView')
router.register('RoomView', RoomFulterSerializer, basename='RoomView')
router.register('ChatView', ChatList, basename='ChatView')
router.register('Notifications', NotificationViewSet, basename='NotificationViewSet')









# urlpatterns = router.urls
urlpatterns=urlpatterns+router.urls


