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
import json

from django.http import Http404, HttpResponse

# university All List
class RoomView(viewsets.ModelViewSet):  
    serializer_class = RoomSerializer   
    queryset = Room.objects.all() 
    
    
# university Arry Description All List

class ChatView(viewsets.ModelViewSet):  
    serializer_class = ChatAllSerializer   
    queryset = Chat.objects.all() 










# class RoomViewSet(viewsets.ModelViewSet):
#     serializer_class = RoomFulterSerializer
#     queryset = Room.objects.all()

# class RoomViewSet(viewsets.ModelViewSet):
#     serializer_class = RoomFulterSerializer
#     queryset = Room.objects.all()

#     def create(self, request, *args, **kwargs):
#         name = request.data.get('name')
#         user_ids = request.data.getlist('user_ids') # Get user_ids array from the request body as a list of integers

#         print("user_id22222222222222222222s",user_ids)
#         description = request.data.get('description', '')        
#         image = request.data.get('image', None)
#         if not name:
#             return Response({'detail': 'Name is required'}, status=status.HTTP_400_BAD_REQUEST)

#         room = Room.objects.create(name=name, description=description, image=image)

#         if user_ids:
#             users = NewUser.objects.filter(id__in=[int(user_id) for user_id in user_ids if user_id.isdigit()])
#             room.users.set(users)
            

#         serializer = self.get_serializer(room)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

from django.core.exceptions import ValidationError

# class RoomViewSet(viewsets.ModelViewSet):
#     serializer_class = RoomFulterSerializer
#     queryset = Room.objects.all()

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             room = serializer.save()

#             user_ids = request.data.getlist('user_ids')
#             user_ids = json.loads(user_ids[0]) if user_ids else []
#             print("user_ids11111",user_ids)
#             if user_ids:
#                 users = NewUser.objects.filter(id__in=user_ids)
#                 room.users.add(*users)

#             serializer = self.get_serializer(room)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# class RoomViewSet(viewsets.ModelViewSet):
#     serializer_class = RoomFulterSerializer
#     queryset = Room.objects.all()
#     lookup_field = 'slug'

#     def create(self, request, *args, **kwargs):
#         try:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)

#             room = serializer.save()

#             user_ids = request.data.getlist('user_ids')
#             user_ids = json.loads(user_ids[0]) if user_ids else []
#             print("user_ids11111",user_ids)
#             if user_ids:
#                 users = NewUser.objects.filter(id__in=user_ids)
#                 room.users.add(*users)

#             serializer = self.get_serializer(room)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except ValidationError as e:
#             return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def update(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             serializer = self.get_serializer(instance, data=request.data, partial=True)
#             serializer.is_valid(raise_exception=True)
#             self.perform_update(serializer)
#             print("serializer.data",serializer.data)
#             return Response(serializer.data)
#         except ValidationError as e:
#             return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def destroy(self, request, *args, **kwargs):
#         try:
#             instance = self.get_object()
#             self.perform_destroy(instance)
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def get_object(self):
#         queryset = self.filter_queryset(self.get_queryset())
#         lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
#         if lookup_url_kwarg in self.kwargs:
#             lookup = self.kwargs[lookup_url_kwarg]
#             if lookup.isdigit():
#                 queryset = queryset.filter(id=lookup)
#             else:
#                 queryset = queryset.filter(**{self.lookup_field: lookup})
#         else:
#             raise Http404
#         try:
#             obj = queryset.get()
#         except queryset.model.DoesNotExist:
#             raise Http404
#         self.check_object_permissions(self.request, obj)
#         return obj







class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = RoomFulterSerializer
    queryset = Room.objects.all()
    lookup_field = 'slug'

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            room = serializer.save()
            user_ids = request.data.getlist('user_ids')
            user_ids = json.loads(user_ids[0]) if user_ids else []
            administrator_ids = request.data.getlist('administrator')
            administrator_ids = json.loads(administrator_ids[0]) if administrator_ids else []
            club_leader_ids = request.data.getlist('club_leader')
            club_leader_ids = json.loads(club_leader_ids[0]) if club_leader_ids else []
            club_coaches_ids = request.data.getlist('club_coaches')
            club_coaches_ids = json.loads(club_coaches_ids[0]) if club_coaches_ids else []
            print("kkkkkkkkkkkkkkkkkkkkkkk",user_ids)
    
            if user_ids:
                room.users.add(*user_ids)
    
            if administrator_ids:
                room.administrator.add(*administrator_ids)
    
            if club_leader_ids:
                room.club_coaches.add(*club_leader_ids)
    
            if club_coaches_ids:
                room.club_leader.add(*club_coaches_ids)
    
            serializer = self.get_serializer(room)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            room = serializer.save()

            user_ids = request.data.getlist('user_ids')
            user_ids = json.loads(user_ids[0]) if user_ids else []
            if user_ids:
                room.users.clear()
                room.users.add(*user_ids)

            serializer = self.get_serializer(room)
            return Response(serializer.data)
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        if lookup_url_kwarg in self.kwargs:
            lookup = self.kwargs[lookup_url_kwarg]
            if lookup.isdigit():
                queryset = queryset.filter(id=lookup)
            else:
                queryset = queryset.filter(**{self.lookup_field: lookup})
        else:
            raise Http404
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404
        self.check_object_permissions(self.request, obj)
        return obj

















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
    

