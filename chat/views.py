from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
from django.contrib.auth.models import User
from users.models import NewUser 
import json


from .models import Chat, Room
from .serializers import ChatSerializer

# Create your views here.
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # print(token)

        token['email'] = user.email

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer














@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createRoom(request):
    if request.method == "POST":
        data = json.loads(request.body)
        try:
            Room.objects.get(name = data['name'], password = data['password'])
            return JsonResponse({"status": 404})
        except:
            Room.objects.create(name = data['name'], password = data['password'])
            return JsonResponse({"status": 200})

# @api_view(['GET', 'POST', 'DELETE'])
# @permission_classes([IsAuthenticated])
# @parser_classes([MultiPartParser, FormParser])
# def room(request, name, password):
#     if request.method == "GET":
#         room = Room.objects.get(name=name, password=password)
#         messages = reversed(room.room.all())
#         serializer = ChatSerializer(messages, many=True)
#         return Response(serializer.data)

#     if request.method == "DELETE":
#         room = Room.objects.get(name=name, password=password)
#         room.delete()

#     if request.method == "POST":
#         print(request.POST, request.data, sep="\n")
#         room = Room.objects.get(name=name, password=password)
#         user = request.user
#         try:
#             message = request.data.get('message')
#         except:
#             message = ""
#         try:
#             image = request.data.get('image')
#             print(image)
#             if image == "undefined":
#                 image = None
#         except:
#             image = None
#         chat = Chat.objects.create(user=user, room=room, message=message, image=image)
#         chat.save()
#         # chat = ChatSerializer(data=request)
#         # chat.user = user
#         # chat.room = room
#         # if chat.is_valid():
#         #     chat.save()
#         return JsonResponse({"status": "201"})



@api_view(['POST'])
def createUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        email = data['email']
        password = data['password']
        try:
            NewUser.objects.get(email=email)
            return JsonResponse({"status": "405", "ok": False})
        except:
            NewUser.objects.create_user(email=email, password=password).save()
            return JsonResponse({"status": "200", "ok": True})









from django.shortcuts import render, get_object_or_404

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@api_view(['GET', 'POST', 'DELETE'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def room(request, name, password):
    room = get_object_or_404(Room, name=name, password=password)
    
    if request.method == "GET":
        messages = reversed(room.room.all())
        serializer = ChatSerializer(messages, many=True)

        # Render the template with the room and messages data
        return render(request, 'chat/room.html', {
            'room_name_json': json.dumps(name),
            'room_messages': json.dumps(serializer.data)
        })

    if request.method == "DELETE":
        room.delete()

        # Notify clients that the room has been deleted
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.name}',
            {
                'type': 'chat.room.deleted',
                'room_name': room.name
            }
        )

        return Response({'detail': 'Room deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)

    if request.method == "POST":
        message = request.data.get('message')

        # Create the message object
        message = Message.objects.create(
            room=room,
            user=request.user,
            message=message
        )

        # Serialize the message object
        serializer = ChatSerializer(message)

        # Send the new message to all clients in the room
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'chat_{room.name}',
            {
                'type': 'chat.message',
                'message': serializer.data
            }
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
