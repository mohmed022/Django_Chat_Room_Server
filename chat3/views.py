from rest_framework import generics
from chat3.models import Room
from chat3.serializers import RoomSerializer
from rest_framework import generics
from chat3.models import Chat ,Notification
from chat3.serializers import ChatSerializer , ChatAllSerializer , RoomFulterSerializer , NotificationSerializer
from rest_framework import viewsets      
from users.models import NewUser
from rest_framework.response import Response
from rest_framework import status


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes
from django.utils import timezone


# university All List
class RoomView(viewsets.ModelViewSet):  
    serializer_class = RoomSerializer   
    queryset = Room.objects.all() 
    
    
# university Arry Description All List

class ChatView(viewsets.ModelViewSet):  
    serializer_class = ChatAllSerializer   
    queryset = Chat.objects.all() 












@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class RoomFulterSerializer(viewsets.ModelViewSet):
    serializer_class = RoomFulterSerializer   

    def get_queryset(self):
        rooms = self.request.user.rooms.all()
        return rooms





def chat_list_by_user_rooms(user):
    # احصل على جميع الغرف التي ينتمي إليها المستخدم
    rooms = user.rooms.all()
    # احصل على جميع الرسائل التي تنتمي إلى الغرف التي يشترك فيها المستخدم
    chats = Chat.objects.filter(room_id__in=rooms)
    
    # قم بترتيب الرسائل بتاريخ الإنشاء
    chats = chats.order_by('-created_at')
    
    return chats

@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
class ChatList(viewsets.ModelViewSet):  
    serializer_class = ChatSerializer   
    queryset = Chat.objects.all()

    def list(self, request, *args, **kwargs):
        # احصل على جميع الرسائل التي تنتمي إلى الغرف التي يشترك فيها المستخدم
        chats = chat_list_by_user_rooms(request.user)
        # قم بتمرير الرسائل إلى السيريالايزر
        serializer = self.get_serializer(chats, many=True)
        # قم بإرجاع البيانات المسلسلة
        return Response(serializer.data)

# class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NotificationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Notification.objects.all()

#     def get_queryset(self):
#         # Filter unread notifications belonging to the current user
#         queryset = self.queryset.filter(user=self.request.user)

#         # Select only the user username and profile picture fields
#         # queryset = queryset.values('user__user_name', 'user__image')

#         # Mark unread notifications as read
#         # queryset.update(is_read=True)

#         return queryset

# class NotificationViewSet(viewsets.ModelViewSet):
#    serializer_class = NotificationSerializer
#    authentication_classes = [JWTAuthentication]
#    permission_classes = [IsAuthenticated]
#    queryset = Notification.objects.all()

#    def get_queryset(self):
#        # Filter notifications belonging to the current user
#        queryset = self.queryset.filter(user=self.request.user)

#        # Mark read notifications for deletion
#        read_notifications = queryset.filter(is_read=True)
#        read_notifications.delete()

#        return queryset.filter(is_read=False)

#    def destroy(self, request, *args, **kwargs):
#        instance = self.get_object()
#        instance.delete()
#        return Response(status=status.HTTP_204_NO_CONTENT)

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()
    lookup_url_kwarg = 'room_id'

    def get_queryset(self):
        # Filter notifications belonging to the current user
        queryset = self.queryset.filter(user=self.request.user)

        # Mark read notifications for deletion
        read_notifications = queryset.filter(is_read=True)
        read_notifications.delete()

        return queryset.filter(is_read=False)
    
    def update(self, request, *args, **kwargs):
        room_id = kwargs['room_id']
        notifications = self.get_queryset().filter(room_id=room_id, is_read=False)
        notifications.update(is_read=True)
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)
    



# class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NotificationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Notification.objects.all()

#     def get_queryset(self):
#         # Filter unread notifications belonging to the current user
#         queryset = self.queryset.filter(user=self.request.user)
        

#         # Mark unread notifications as read
#         # queryset.update(is_read=True)

#         # Filter notifications created today
#         # today = timezone.now().date()
#         # queryset = queryset.filter(created_at__date=today)

#         return queryset
    
# class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
#     serializer_class = NotificationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]
#     queryset = Notification.objects.all()

#     def get_queryset(self):
#         # تصفية الإشعارات غير المقروءة والتي تنتمي إلى المستخدم الحالي
#         queryset = self.queryset.filter(user=self.request.user, is_read=False)

#         # تحديث الإشعارات غير المقروءة لتصبح مقروءة
#         queryset.update(is_read=True)

#         # تصفية الإشعارات التي تم إنشاؤها في اليوم الحالي فقط
#         today = timezone.now().date()
#         queryset = queryset.filter(created_at__date=today)

#         return queryset

# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# class NotificationViewSet(viewsets.ModelViewSet):
#     serializer_class = NotificationSerializer
#     queryset = Chat.objects.all()
    
#     def list(self, request, *args, **kwargs):
#         # احصل على جميع الرسائل التي تنتمي إلى الغرف التي يشترك فيها المستخدم
#         queryset = Notification.objects.filter(user=self.request.user)

#         return queryset
    

    # def get_queryset(self):
    #     queryset = Notification.objects.filter(user=self.request.user)
    #     return queryset

    
# from rest_framework import viewsets, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import JWTAuthentication
# from rest_framework.response import Response
# from .models import Notification
# from .serializers import NotificationSerializer

# class NotificationViewSet(viewsets.ModelViewSet):
#     serializer_class = NotificationSerializer
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         queryset = Notification.objects.filter(user=self.request.user)
#         return queryset

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def partial_update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         self.perform_destroy(instance)
#         return Response(status=status.HTTP_204_NO_CONTENT)
