# from asgiref.sync import sync_to_async
# from channels.generic.websocket import JsonWebsocketConsumer
# from django.contrib.auth import get_user_model
# import jwt
# from .models import NewUser


# class OnlineUsersConsumer(JsonWebsocketConsumer):
#     async def connect(self):
#         try:
#             token = self.scope['query_string'].decode().split("=")[1]
#             user_id = jwt.decode(token, 'secret', algorithms=['HS256'])['user_id']
#             self.user_id = user_id
#             user = await sync_to_async(get_user_model().objects.filter(id=user_id).first)()
#             if user:
#                 self.scope['user'] = user
#         except Exception as e:
#             print("Error authenticating user: ", e)
#             await self.close()

#         self.room_group_name = "status_user"
#         await self._add_to_group()
#         await self._send_initial_payload()
#         await self.accept()
        

#     async def _add_to_group(self):
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def _send_initial_payload(self):
#         users = await self._get_users()
#         await self.send_json({
#             'type': 'user_all_notification',
#             'users': list(users)
#         })

#     async def _get_users(self):
#         users = await sync_to_async(NewUser.objects.all().order_by('-id').values)('id', 'email', 'user_name', 'image', 'is_online')
#         return users


#     async def disconnect(self, close_code):
#         await self.update_user_status(False)
#         print(f"Disconnected: {close_code}")



#     async def update_user_status(self, is_online):
#         await sync_to_async(NewUser.objects.filter(id=self.user_id).update)(is_online=is_online)
#         user = await sync_to_async(NewUser.objects.filter(id=self.user_id).order_by('id').values)('id', 'email', 'user_name', 'image', 'is_online')
#         for obj in user:
#             id = obj['id']
#             user_name = obj['user_name']
#             image = obj['image']
#             is_online = obj['is_online']
#             email = obj['email']
#             self.room_group_name = f"status_user"
#             await self.channel_layer.group_send(
#                 self.room_group_name,
#                 {
#                     'type': 'user_online_notification',
#                     'id': id,
#                     'user_name': user_name,
#                     'image': image,
#                     'email': email,
#                     'is_online': is_online
#                 }
#             )

#     async def user_online_notification(self, event):
#         await self.send_json({
#             'type': 'user_online_notification',
#             'id': event['id'],
#             'user_name': event['user_name'],
#             'image': event['image'],
#             'email': event['email'],
#             'is_online': event['is_online']
#         })

#     async def user_all_notification(self, event):
#         await self.send_json({
#             'type': 'user_all_notification',
#             'users': event['users']
#         })






































    # def send_all_users(self):
    #     users = NewUser.objects.all().order_by('-id').values('id', 'email', 'user_name', 'image', 'is_online')
    #     async_to_sync(self.send_json)({
    #         'type': 'user_all_notification',
    #         'users': list(users)
    #     })
    





# import logging
# from urllib.parse import parse_qs
# from channels.generic.websocket import AsyncWebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.conf import settings
# from .models import NewUser

# logger = logging.getLogger(__name__)
# import jwt
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# def get_user_from_token(token):
#     User = get_user_model()

#     try:
#         decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#         user_id = decoded_token.get('user_id')
#         user = User.objects.get(pk=user_id)
#         return user
#     except (InvalidToken, TokenError, User.DoesNotExist):
#         return None


# class OnlineUsersConsumer(AsyncWebsocketConsumer):

#     async def connect(self):
#         try:
#             self.user_online = self.scope['url_route']['kwargs']['user_online']
#             self.room_group_name = 'chat_%s' % self.user_online

#             # Get token from query string
#             query_string = self.scope['query_string'].decode()
#             params = parse_qs(query_string)
#             token = params.get('token', [None])[0]

#             # Get user information from token
#             user = get_user_from_token(token)

#             # Check if user is authenticated
#             if user is not None:
#                 self.user_id = user['user_id']
#                 self.user_name = user['user_name']
#                 self.email = user['email']
#                 self.is_online = user['is_online']
#                 NewUser.objects.filter(id=self.user_id).update(is_online=True)
#                 logger.info("User {} is online".format(self.user_name))

#                 # Join room group
#                 await self.channel_layer.group_add(
#                     self.room_group_name,
#                     self.channel_name
#                 )

#                 # Initialize list to keep track of sent user_in_loops
#                 self.sent_users_online = []

#                 old_users_online = NewUser.objects.filter(is_online=True).order_by('id')

#                 # Send old users_online to the client
#                 for user_in_loop in old_users_online:
#                     # Check if user_in_loop has already been sent
#                     if user_in_loop.id not in self.sent_users_online:
#                         await self.channel_layer.group_send(
#                             self.room_group_name,
#                             {
#                                 'type': 'user_online_in_loop',
#                                 'id': user_in_loop.id,
#                                 'user_name': user_in_loop.user_name,
#                                 'image': user_in_loop.image.url if user_in_loop.image else None,
#                                 'created_at': user_in_loop.created_at.replace(tzinfo=None).strftime('%H:%M:%S'),
#                                 'site_url': settings.SITE_URL,
#                             }
#                         )
#                         # Add sent user_in_loop ID to list
#                         self.sent_users_online.append(user_in_loop.id)
#             else:
#                 self.user_id = None
#                 self.user_name = 'Anonymous'
#                 self.email = None

#             await self.accept()

#         except Exception as e:
#             logger.error("Error connecting websocket: {}".format(str(e)))
#             await self.close()

#     async def disconnect(self, close_code):
#         if self.user_id is not None:
#             NewUser.objects.filter(id=self.user_id).update(is_online=False)
#             logger.info("User {} is offline".format(self.user_name))

#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         pass


#     async def user_online_in_loop(self, event):
#         try:
#             user_name = event['user_name']
#             image = event['image']
#             created_at = event['created_at']
#             site_url = event['site_url']
    
#             await self.send(text_data='{"type": "user_in_loop", "user_name": "' + user_name + '", "image": "' + str(image) + '", "created_at": "' + created_at + '", "site_url": "' + site_url + '"}')
#         except Exception as e:
#             # Handle the error here
#             print(f"An error occurred while sending user_in_loop message: {e}")





from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

class Mytest(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        await self.send(text_data="You are connected!")

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        await async_to_sync(self.handle_message)(text_data)

    def handle_message(self, text_data):
        self.send(text_data=text_data)



















from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder

import io
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from users.models import NewUser
import base64
from datetime import datetime
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings




from channels.layers import get_channel_layer
from django.dispatch import receiver
from django.db.models.signals import post_save






from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import json
import io
import base64
from datetime import datetime
import uuid



from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
import json
import io
import os
import base64
from datetime import datetime

import uuid
from urllib.parse import parse_qs
import jwt
from django.conf import settings
import logging
import json




logger = logging.getLogger(__name__)

# Decode JWT token and extract user information
def get_user_from_token(token):
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        user_name = payload.get('user_name')
        email = payload.get('email')
        is_online=payload.get('is_online')
        # print(user_id ,user_name , email , is_online , "JWT token")
        # ... extract other user information from the payload as needed
        return {'user_id': user_id, 'user_name': user_name, 'email': email , 'is_online':is_online}
    except jwt.exceptions.DecodeError:
        # Invalid token
        return None
    except jwt.exceptions.ExpiredSignatureError:
        # Token has expired
        return None

def get_room_group_name(self):
    return f"users_{self.user_id}"

class OnlineUsersConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id = None
    
    def connect(self):
        try:
            query_string = self.scope['query_string'].decode()
            params = parse_qs(query_string)
            token = params.get('token', [None])[0]

            user = get_user_from_token(token)

            if user is not None:
                self.user_id = user['user_id']
                self.user_name = user['user_name']
                self.email = user['email']
                self.is_online = user['is_online']
                # NewUser.objects.filter(id=self.user_id).update(is_online=True)
                self.update_user_to_online(is_online=True)
                # self.receive(self.user_id)
                self.room_group_name = f"statu_user"
                async_to_sync(self.channel_layer.group_add)(
                    self.room_group_name,
                    self.channel_name
                )

                self.Sent_UsersOnlien = []

                old_users_online = NewUser.objects.filter(is_online=True).order_by('id')

                for user_in_loop in old_users_online:
                    if user_in_loop.id not in self.Sent_UsersOnlien:
                        async_to_sync(self.channel_layer.group_send)(
                            self.room_group_name,
                            {
                                'type': 'user_online_notification',
                                'id': user_in_loop.id,
                                'user_name': user_in_loop.user_name,
                                'image': user_in_loop.image.url if user_in_loop.image else None,
                                'email': user_in_loop.email ,
                                'is_online': user_in_loop.is_online ,
                            }
                        )
                        self.Sent_UsersOnlien.append(user_in_loop.id)
                        # user = get_user_from_token(self.Sent_UsersOnlien)

            else:
                self.user_name = 'Anonymous'
                self.email = None

            self.accept()
        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error connecting to websocket: {str(e)}")




    def disconnect(self, close_code):
        try:
            # Leave room group
            self.update_user_to_offline(is_online=False)
            if self.room_group_name is not None:
                async_to_sync(self.channel_layer.group_discard)(
                    # use room_group_name                
                    self.room_group_name,
                    self.channel_name
                )
        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error disconnecting user: {str(e)}")
    
        
    def receive(self, text_data):
        # print(self.user_id,"self.user_id")
        try:
            text_data_json = json.loads(text_data)
            user = NewUser.objects.filter(id=self.user_id).order_by('id').values('id', 'email', 'user_name', 'image', 'is_online')
            
            for obj in user: 
                id=obj['id'] 
                user_name = obj['user_name']
                image = obj['image']
                is_online = obj['is_online']
                email = obj['email']
            
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'user_online_notification',
                    'id': id,
                    'user_name': user_name,
                    'image': image,
                    'is_online': is_online,
                    'email': email,
                }
            )
    
        except Exception as e:
            # Handle the exception here
            print(f"An error occurred: {e}")
            self.send(text_data=json.dumps({'error': "Something went wrong"}))


     

 
    def update_user_to_online(self, is_online):
        #  print("update_user_to_online" , is_online)
         try:
             # Check current user status
             current_status = NewUser.objects.filter(id=self.user_id, is_online=is_online).exists()    
             # If current status is not equal to new status
             if not current_status:
                 
                 # Update user status
                 NewUser.objects.filter(id=self.user_id).update(is_online=is_online)
    
                 # Get user data
                 user = NewUser.objects.filter(id=self.user_id).order_by('id').values('id', 'email', 'user_name', 'image', 'is_online')
                 for obj in user:
                     id = obj['id']
                     user_name = obj['user_name']
                     image = obj['image']
                     is_online = obj['is_online']
                     email = obj['email']
    
                     # Send notification to all users in the room
                     if is_online:
                         self.room_group_name = f"statu_user"
                         async_to_sync(self.channel_layer.group_send)(
                             self.room_group_name,
                             {
                                 'type': 'user_online_notification',
                                 'id': id,
                                 'user_name': user_name,
                                 'image': image,
                                 'email': email,
                                 'is_online': is_online
                             }
                         )
         except Exception as e:
             # Handle any exceptions that might occur
             print(f"Error updating user status: {str(e)}")
             
             
    def user_online_notification(self, event):
        # print("user_online_notification" , event)
        logger.info("user_online_notification called with event: %s", event)
        try:
            # Get notification data
            id = event['id']
            user_name = event['user_name']
            image = event['image']
            is_online = event['is_online']
            email = event['email']
            if is_online :
                # Send notification to all users in the room
                self.send(text_data=json.dumps({
                    'type': 'user_online_notification',
                    'id': id,
                    'user_name': user_name,
                    'image': image,
                    'is_online': is_online,
                    'email': email,
                }))
        except KeyError as e:
            logger.error("Error in user_online_notification: %s", str(e))
    
    

    def update_user_to_offline(self, is_online):
        try:
            # Check current user status
            current_status = NewUser.objects.filter(id=self.user_id, is_online=is_online).exists()
            # print("current_status" , current_status)    
            
            # If current status is not equal to new status
            if not current_status:
                # Update user status
                NewUser.objects.filter(id=self.user_id).update(is_online=is_online)

                # Get user data
                user = NewUser.objects.filter(id=self.user_id).order_by('id').values('id', 'email', 'user_name', 'image', 'is_online')
                for obj in user:
                    id = obj['id']
                    user_name = obj['user_name']
                    image = obj['image']
                    is_online = obj['is_online']
                    email = obj['email']
                    # print("current_status => id" , id)    
                    

                    # Send notification to all users in the room
                    self.room_group_name = f"statu_user"
                    async_to_sync(self.channel_layer.group_send)(
                        self.room_group_name,
                        {
                            'type': 'user_offline_notification',
                            'id': id,
                            'user_name': user_name,
                            'image': image,
                            'email': email,
                            'is_online': is_online,    
                        }
                    )
                    # print("current_status => is_online" , is_online)

        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error updating user status: {str(e)}")
           
    #         llllllllllllllllllllllllllllllllllllllllllllllllll
            
            
    

            
    
    
    def user_offline_notification(self, event):
        # print("user_offline_notification" , event)
        logger.info("user_offline_notification called with event: %s", event)
        try:
            # Get notification data
            id = event['id']
            user_name = event['user_name']
            image = event['image']
            is_online = event['is_online']
            email = event['email']
            # print ("is_online off " ,is_online)
            self.send(text_data=json.dumps({
                'type': 'user_offline_notification',
                'id': id,
                'user_name': user_name,
                'image': image,
                'is_online': is_online,
                'email': email,
            }))
        except KeyError as e:
            logger.error("Error in user_offline_notification: %s", str(e))
        
        
        
        
        
        
        
    # def update_user_status(self, is_online):
    #  try:
    #      # Update user status
    #      NewUser.objects.filter(id=self.user_id).update(is_online=is_online)
     
    #      # Get user data
    #      user = NewUser.objects.filter(id=self.user_id).order_by('id').values('id', 'email', 'user_name', 'image', 'is_online')
    #      for obj in user:
    #          id = obj['id']
    #          user_name = obj['user_name']
    #          image = obj['image']
    #          is_online = obj['is_online']
    #          email = obj['email']
     
    #          # Send notification to all users in the room
    #          if is_online:
    #              self.room_group_name = f"statu_user"
    #              async_to_sync(self.channel_layer.group_send)(
    #                  self.room_group_name,
    #                  {
    #                      'type': 'user_online_notification',
    #                      'id': id,
    #                      'user_name': user_name,
    #                      'image': image,
    #                      'email': email,
    #                      'is_online': True
    #                  }
    #              )
    #          else:
    #              self.room_group_name = f"statu_user"
    #              async_to_sync(self.channel_layer.group_send)(
    #                  self.room_group_name,
    #                  {
    #                      'type': 'user_ofline_notification',
    #                      'id': id,
    #                      'user_name': user_name,
    #                      'image': image,
    #                      'email': email,
    #                      'is_online': False
    #                  }
    #              )
    #  except Exception as e:
    #      # Handle any exceptions that might occur
    #      print(f"Error updating user status: {str(e)}")
    
    
    
    
        
        
            # def get_notification_data(event):
    #     """
    #     Get notification data from event.
    #     """
    #     return {
    #         'user_name': event['user_name'],
    #         'image': event['image'],
    #         'is_online': event['is_online'],
    #         'email': event['email'],
    #         'type': event.get('type', ''),
    #     }
    
    
    # def get_all_users():
    #     """
    #     Get all users from the database.
    #     """
    #     return [user for user in NewUser.objects.all().values()]
    
    
    # def send_user_all_notification(self, all_users):
    #     """
    #     Send notification to requesting user with all users.
    #     """
    #     self.send(text_data=json.dumps({
    #         'type': 'user_all_notification',
    #         'users': all_users,
    #     }))
    
    
    # def send_user_online_notification(self, notification_data):
    #     """
    #     Send notification to all users in the room when a user joins the room.
    #     """
    #     notification_data['type'] = 'user_online_notification'
    #     self.send(text_data=json.dumps(notification_data))
    
    
    # def send_user_offline_notification(self, notification_data):
    #     """
    #     Send notification to all users in the room when a user leaves the room.
    #     """
    #     notification_data['type'] = 'user_offline_notification'
    #     self.send(text_data=json.dumps(notification_data))
    
    
    # def user_online_notification(self, event):
    #     """
    #     Send notification to all users in the room when a user joins or leaves the room.
    #     """
    #     # Get notification data
    #     notification_data = self.get_notification_data(event)
        
    #     # Check the type of notification
    #     notification_type = notification_data['type']
        
    #     if notification_type == 'user_all_notification':
    #         # Get all users from the database
    #         all_users = self.get_all_users()
    #         self.send_user_all_notification(self, all_users)
    #     elif notification_data['is_online']:
    #         # Send notification to all users in the room when a user joins the room
    #         self.send_user_online_notification(self, notification_data)
    #     else:
    #         # Send notification to all users in the room when a user leaves the room
    #         self.send_user_offline_notification(self, notification_data)
    
        
        
        
        
        
        
        
        
        
        
        
        


    # def user_online_in_loop(self, event):
    #     # print(event,"state_user_in_loop")
    #     try:
    #         if 'id' not in event:
    #             raise ValueError("'id' key is not present in event")


    #         id = event['id']
    #         user_name = event['user_name']
    #         image = event['image']
    #         is_online = event['is_online']
    #         email = event['email']
    #         # print(image_url)
    #         # created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
          
    #         # Send user_in_loop to WebSocket
    #         self.send(text_data=json.dumps({
    #             'type': 'user_online_in_loop',
    #             'id': id,
    #             'user_name': user_name,
    #             'image': image,
    #             'is_online': is_online,
    #             'email': email,
    #         }, cls=DjangoJSONEncoder))
   
    #     except KeyError as e:
    #         # Handle the KeyError exception
    #         print(f"KeyError occurred: {e}")
    #         self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))

    #     except Exception as e:
    #         # Handle any other exception
    #         print(f"An error occurred: {e}")
    #         self.send(text_data=json.dumps({'error': str(e)}))
    # def update_user_status(self, is_online):
    #     NewUser.objects.filter(id=self.user_id).update(is_online=is_online)
    #     user = NewUser.objects.filter(id=self.user_id).order_by('id').values('id', 'email', 'user_name', 'image', 'is_online')
    #     for obj in user:
    #         id = obj['id']
    #         user_name = obj['user_name']
    #         image = obj['image']
    #         is_online = obj['is_online']
    #         email = obj['email']
    #         print(is_online, " 555555555555555555666666666666666666")
            
        # self.send(text_data=json.dumps({
        #         'type': 'user_online_in_loop',
        #         'id': id,
        #         'user_name': user_name,
        #         'image': image,
        #         'is_online': is_online,
        #         'email': email,
        #     }, cls=DjangoJSONEncoder))
        
        # async_to_sync(self.channel_layer.group_discard)(
        #     self.room_group_name,
        #     self.channel_name
        # )

    
# class OnlineUsersConsumer(WebsocketConsumer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.user_id = None

#     def connect(self):
#         self.user_online = self.scope['url_route']['kwargs']['user_online']
#         self.room_group_name = 'chat_%s' % self.user_online

#         query_string = self.scope['query_string'].decode()
#         params = parse_qs(query_string)
#         token = params.get('token', [None])[0]

#         user = get_user_from_token(token)

#         if user is not None:
#             self.user_id = user['user_id']
#             self.user_name = user['user_name']
#             self.email = user['email']
#             self.is_online = user['is_online']
#             NewUser.objects.filter(id=self.user_id).update(is_online=True)

#             async_to_sync(self.channel_layer.group_add)(
#                 self.room_group_name,
#                 self.channel_name
#             )

#             self.Sent_UsersOnlien = []

#             old_users_online = NewUser.objects.filter(is_online=True).order_by('id')

#             for user_in_loop in old_users_online:
#                 if user_in_loop.id not in self.Sent_UsersOnlien:
#                     async_to_sync(self.channel_layer.group_send)(
#                         self.room_group_name,
#                         {
#                             'type': 'user_online_in_loop',
#                             'id': user_in_loop.id,
#                             'user_name': user_in_loop.user_name,
#                             'image': user_in_loop.image.url if user_in_loop.image else None,
#                             # 'created_at': user_in_loop.created_at.replace(tzinfo=None).strftime('%H:%M:%S'),
#                             'site_url': settings.SITE_URL,
#                         }
#                     )
#                     self.Sent_UsersOnlien.append(user_in_loop.id)
#         else:
#             self.user_name = 'Anonymous'
#             self.email = None

#         self.accept()


#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )
#         NewUser.objects.filter(id=self.user_id).update(is_online=False)
          


#     def receive(self, text_data):
#         pass


    
#     def user_online_in_loop(self, event):
#         print(event,"state_user_in_loop")
#         try:
#             if 'id' not in event:
#                 raise ValueError("'id' key is not present in event")


#             user_id = event['id']
#             user_name = event['user_name']
#             image_url = event['image']
#             # created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
          
#             # Send user_in_loop to WebSocket
#             self.send(text_data=json.dumps({
#                 'id': user_id,
#                 'image': image_url,
#                 'user_name':user_name,
#             }, cls=DjangoJSONEncoder))
   
        # except KeyError as e:
        #     # Handle the KeyError exception
        #     print(f"KeyError occurred: {e}")
        #     self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))

        # except Exception as e:
        #     # Handle any other exception
        #     print(f"An error occurred: {e}")
        #     self.send(text_data=json.dumps({'error': str(e)}))


