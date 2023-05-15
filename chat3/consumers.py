from django.core.serializers.json import DjangoJSONEncoder
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from users.models import NewUser
from datetime import datetime
from django.conf import settings
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from django.conf import settings
from .models import Chat, Room , vote , Voting_Questions , Notification
from urllib.parse import parse_qs
import jwt
import re   # للتعرف علي ارقام الهواتق والروابط واخفائها
from django.forms.models import model_to_dict



# class ChatConsumer(AsyncWebsocketConsumer):
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.extract_user_info()
        self.join_room_group()
        self.handell_activeChat_in_link("activeChat")
        self.accept()
        # print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    
    def handell_activeChat_in_link(self , activeChat):
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        activeChat = params.get(activeChat, [None])[0]
        if activeChat :
            self.update_user_chat_room_status(activeChat)
            # self.update_msg_room_status(activeChat)
            

    
    # def update_msg_room_status(self, activeChat):
    #     # التحقق من وجود رسائل غير مقروءة
    #     messages = Chat.objects.filter(room_id=activeChat, user_to=self.user_id, is_read=False)
    #     if messages:
    #         # تحديث جميع الرسائل في نفس الوقت
    #         updated_messages_ids = list(messages.values_list('id', flat=True))
    #         messages.update(is_read=True)
    #         async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #             {
    #                 'type': 'chat_message_update_is_read',
    #                 'updated_messages_ids': updated_messages_ids,
    #             }
    #         )
    #     else:
    #         print("No messages to update")
    # def update_msg_room_status(self, activeChat):
    #     # التحقق من وجود رسائل غير مقروءة
    #     messages = Chat.objects.filter(room_id=activeChat, user_to__id=self.user_id, is_read=False)
    #     # if messages:
    #         # تحديث جميع الرسائل في نفس الوقت
    #     updated_messages_ids = list(messages.values_list('id', flat=True))
    #     messages.update(is_read=True)
    #     async_to_sync(self.channel_layer.group_send)(
    #         self.room_group_name,
    #         {
    #             'type': 'chat_message_update_is_read',
    #             'updated_messages_ids': updated_messages_ids,
    #             'state':"true",
    #         }
    #     )
    #     # else:
    #     #     print("No messages to update")
    
    # def chat_message_update_is_read(self, event):
    #     print(event)
    #     updated_messages_ids = event['updated_messages_ids']

    #     # إرسال التحديث إلى جميع المتصلين بالغرفة
    #     self.send(text_data=json.dumps({
    #         'type': 'chat_message_update_is_read',
    #         'updated_messages_ids': updated_messages_ids,
    #     }, cls=DjangoJSONEncoder))
    ids_masege = []
    def update_msg_room_status(self, activeChat):
        try:
            # التحقق من وجود رسائل غير مقروءة
            messages = Chat.objects.filter(room_id=activeChat, user_to__id=self.user_id, is_read=False)
            # تحديث جميع الرسائل في نفس الوقت
            if messages :
                messages.update(is_read=True)
                updated_messages = list(messages.values_list('id', flat=True))
                print("true messages")
            messages2 = Chat.objects.filter(room_id=activeChat, user_id__id=self.user_id, is_read=True)
            if messages2:
                updated_messages2 = list(messages2.values_list('id', flat=True))
                print("true messages2")
                        
            
            
            if updated_messages:
                updated_messages_ids = updated_messages
                is_read = True
            elif updated_messages2:
                updated_messages_ids = updated_messages2
                is_read = True
            else:
                updated_messages_ids = []
                is_read = False
            
            print("updated_messages_ids",is_read , updated_messages_ids)
            # إرسال التحديث إلى جميع المتصلين بالغرفة
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {
                    'type': 'chat_message_update_is_read',
                    'is_read': is_read,
                    'updated_messages_ids': updated_messages_ids,
                    'room_id': activeChat,
                }
            )

        except Exception as e:
            print("Error occurred while updating message status: ", e)
    
    def chat_message_update_is_read(self, event):
        try:
            # updated_messages_ids = event['updated_messages_ids']
            is_read = event.get('is_read', '')
            room_id = event.get('room_id', '')
            updated_messages_ids = event.get('updated_messages_ids', [])

            
            # إرسال التحديث إلى جميع المتصلين بالغرفة
            self.send(text_data=json.dumps({
                'type': 'chat_message_update_is_read',
                'updated_messages_ids': updated_messages_ids,
                'is_read': is_read,
                'room_id': room_id,
            }, cls=DjangoJSONEncoder))
        except Exception as e:
            print("Error occurred while sending message update: ", e)
    
    


        
    # def filter_users(self):
    #     room_obj = self.get_data_in_this_room(self.room_name)
    #     # استرداد جميع المستخدمين في الغرفة
    #     room_users = self.get_users_in_room(room_obj)
    #     # تصفية المستخدمين والت...
    #     return [str(user_id) for user_id in room_users if user_id != self.user_id]
    
    
    
    
        
        
        
        
        
    
    def handell_token_in_link(self):
        query_string = self.scope['query_string'].decode()
        params = parse_qs(query_string)
        token = params.get('token', [None])[0]
        return token
        
    def get_user_id_from_token(self , token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload.get('user_id')         
            return {"user_id":user_id}
        except jwt.exceptions.DecodeError:
            # Invalid token
            return None
        except jwt.exceptions.ExpiredSignatureError:
            # Token has expired
            return None
        
    def extract_user_info(self):
        token = self.handell_token_in_link()
        user_id = self.get_user_id_from_token(token)
        
        if user_id is not None:
            self.user_id = user_id['user_id']
        else:
            self.user_id = None
        print("self-user",self.user_id)
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.room_only_user = self.create_user_room()
        # self.room_only_user = 'chat_%s' % self.room_name
        
    def join_room_group(self):
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name,
        )

    def create_user_room(self):
        channel_layer = get_channel_layer()
        room_only_user = f"user_{self.user_id}"
        async_to_sync(channel_layer.group_add)(
            room_only_user,
            self.channel_name,
        )
        return room_only_user
    

    def disconnect(self, close_code):
        # Leave room group
        print("desconected" , self.user_id)
        print("llllllllllllllllllllllllllll")
        
        self.update_user_chat_room_status(0)
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )
        async_to_sync(self.channel_layer.group_discard)(
            self.room_only_user,
            self.channel_name
        )

    def get_data_user_join_naw(self , user_id):
        try:
            user = NewUser.objects.filter(id=user_id).first()
            if user:
                user_data = {
                    'id': user.id,
                    'user_name': user.user_name,
                    'image': user.image.url if user.image else None,
                    'is_online': user.is_online,
                    'is_activeChat':user.is_activeChat,
                }
                return user_data
            else:
                raise ValueError("User does not exist")
        except Exception as e:
            print(f"An error occurred: {e}")
            return {'error': 'Something went wrong'}

    def get_data_in_this_room(self , room):
        try:
            room_obj = Room.objects.get(name=room)
            return room_obj
        except Room.DoesNotExist:
            raise ValueError("Room does not exist")

    def get_users_in_room(self, room_obj):
        if room_obj:
            users_list = [user.id for user in room_obj.users.all()]
            return users_list
        return []
    
    def get_other_users_in_room_only_first(self, room_obj):
        if room_obj:
            users_list = [user.id for user in room_obj.users.all() if user.id != self.user_id]
            return users_list[0] if users_list else None
        return None
    

    
    def handell_message(self, message_in_user):
        # Check for bad words
        bad_words = ['احا', 'احاا', 'احااا']
        for word in bad_words:
            if word in message_in_user.lower():
                message_in_user = message_in_user.replace(word, '*' * len(word))
        return message_in_user
        


    
    def save_chat(self, message, image, room_obj, other_users, vote_data):
        try:
            if vote_data and vote_data.get('discussion_topic', ''):
                discussion_topic = vote_data.get('discussion_topic', '')
                description_discussion = vote_data.get('description_discussion', '')
                voting_questions = vote_data.get('voting_questions', [])
                if voting_questions:
                    voting_questions_data = []
                    for question in voting_questions:
                        question_text = next(iter(question.values()))
                        VotingQuestion = Voting_Questions.objects.create(question=question_text)
                        voting_questions_data.append(VotingQuestion)
                        
                        
                    # Vote_data.voting_questions.set(voting_questions_data)
                    
                    Vote_data = vote.objects.create(discussion_topic=discussion_topic, 
                                                    description_discussion=description_discussion,
                                                    )
                    Vote_data.user_id.set([self.user_id])
                    Vote_data.voting_questions.set(voting_questions_data)
                    print("VotingQuestion",voting_questions_data)

                    
                    chat = Chat.objects.create(room_id=room_obj, vote=Vote_data)
                    if chat is not None:
                        chat.user_id.set([self.user_id])
                else:
                    chat = Chat.objects.create(room_id=room_obj)
                    if chat is not None:
                        chat.user_id.set([self.user_id])
            elif message and message.strip() and not image:
                chat = Chat.objects.create(room_id=room_obj, message=message)
                if chat is not None:
                    chat.user_id.set([self.user_id])
            elif image:
                chat = Chat.objects.filter(id=image).first()
                if chat:
                    print("image", chat)
                else:
                    print("image", "else")
            else:
                chat = None
            return chat
        except NewUser.DoesNotExist:
            print(f"User with id {other_users} does not exist.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
        
        
    def save_notification(self, user_id, message, chat):
        
        try:
            if message:
                new_user = NewUser.objects.get(id=user_id)
                new_chat = Chat.objects.get(id=chat.id)
                new_user_created = NewUser.objects.get(id=self.user_id)
                nuw_room_id = Room.objects.get(id=new_chat.room_id.id)
                notification = Notification.objects.create(user=new_user, user_created=new_user_created , chat=new_chat, room_id=nuw_room_id , message=message)
                return notification
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
              
    def handle_send_msg_or_navgaction(self, room_users, message, chat, user_obj):
        try:
            for user_id in room_users:
                user = NewUser.objects.filter(id=user_id).first()
                room_id = int(chat.room_id.id)
                room_name = chat.room_id.name
                if user:
                    is_active_chat = user.is_activeChat
                    if int(is_active_chat) != chat.room_id.id:
                        # print(f"False: is_active_chat ({is_active_chat}) != chat.room_id.id ({chat.room_id.id})", )
                        notification = self.save_notification(user_id, message, chat)
                        get_and_send_nof = self.send_notification_to_user(notification, user_obj, user.id , room_id , room_name)

            return True
        except Exception as e:
            print(f"Error in handle_send_msg_or_navgaction: {str(e)}")
            return False
    
    def send_notification_to_user(self, notification, user_obj, user_id , room_id , room_name):
        if notification.user and notification.user.id == user_id:            
            try:
                get_id_notification = Notification.objects.filter(message=notification.message , chat=notification.chat.id , user_id=user_id ).first()
                if get_id_notification:
                    room_only_user = f'user_{user_id}'
                    async_to_sync(self.channel_layer.group_send)(
                         room_only_user ,{
                            'type':'send_notification',
                            'state':'notification',
                            'id':get_id_notification.id,
                            'room_id': get_id_notification.room_id.id,
                            'room_name':get_id_notification.room_id.name,
                            'is_read': get_id_notification.is_read,
                            'message': notification.message if hasattr(notification, 'message') else '',
                            'user_name_to': notification.user.user_name if hasattr(notification.user, 'user_name') else '',
                            'chat': notification.chat.id if hasattr(notification, 'chat') else '',
                            'user_id': user_id,
                            'user_name': user_obj['user_name'],
                            'user_image': user_obj['image'] if user_obj['image'] else None,
                            'image': notification.chat.image.url if hasattr(notification.chat, 'image') and notification.chat.image else None,
                        } 
                    )
                    print("Notification sent successfully to user", f'user_{user_id}' , 1)
            except Exception as e:
                print(f"Failed to send notification, {e}")    
        else:
            print("No notification sent")
    # تحديد قائمة لتخزين حالات الإشعارات المرسلة
    sent_notifications = []

    def send_notification(self, event):
        # print("Sending notification", event)
        try:
            # فحص ما إذا كان الإشعار قد تم إرساله مسبقًا
            if event['id'] in self.sent_notifications:
                return
            image_url = event.get('user_image', None)
            if image_url:
                image_url = settings.SITE_URL + image_url

            self.send(text_data=json.dumps({
                'type': 'send_notification',
                'id': event['id'],
                'room_id':event['room_id'],
                'room_name':event['room_name'],
                'is_read':event['is_read'],
                'message': event['message'],
                'user_name_to': event['user_name_to'],
                'chat': event['chat'],
                'user_id': event['user_id'],
                'user_name': event['user_name'],
                'user_image':image_url,
                'image': event['image'],
            }))
            # إضافة الإشعار إلى قائمة الإشعارات المرسلة
            self.sent_notifications.append(event['id'])
            print("Notification sent successfully to", self.room_only_user)
        except Exception as e:
            # إضافة معالجة للأخطاء
            print(f"Failed to send notification, {e}")

    # يمكن إضافة handler أخرى لمعالجة الأخطاء
    def handle_errors(self, event):
        print(f"Error occurred: {event}")
        # يمكن إرسال رسالة خطأ إلى العميل
        self.send(text_data=json.dumps({
            'type': 'error',
            'message': f"Error occurred: {event}",
        }))


    

    
  
    def ADD_USER_TO_QUESTION(self, room_id , msg_id, room ,  questions_id , UserFulterArry_id):
        print("questions_id",questions_id)
        print("UserFulterArry_id",UserFulterArry_id)
        room_obj = self.get_data_in_this_room(room)
        user_obj = self.get_data_user_join_naw(self.user_id) 
        room_users = self.get_users_in_room(room_obj)
        
        voting_question = Voting_Questions.objects.get(id=questions_id)
        if voting_question.list_of_people_who_vote.filter(id=UserFulterArry_id).exists():
            voting_question.list_of_people_who_vote.remove(UserFulterArry_id)
        else:
            voting_question.list_of_people_who_vote.add(UserFulterArry_id)
        voting_question.save()
        chat = Chat.objects.get(id=msg_id)
        response_data = {
            'type': 'edite.message',
            'voting_question': voting_question.id,
            'msg_id':msg_id,
            'room_id':room_id
        }
        # if chat:
        #     response_data['id'] = chat.id
        
        # if chat and hasattr(chat, 'vote'):
        #     vote_dict = model_to_dict(chat.vote) if chat.vote else {}
        #     vote_dict['files'] = str(vote_dict['files']) if vote_dict.get('files') else ''
        #     vote_dict['image'] = str(vote_dict['image']) if vote_dict.get('image') else ''
        #     voting_questions = vote_dict.get('voting_questions', [])
        #     print("voting_questions",voting_questions)

        #     vote_dict['voting_questions'] = [model_to_dict(question) for question in voting_questions]
            
        #     vote_dict['user_id'] = [model_to_dict(user) for user in vote_dict['user_id']] if vote_dict.get('user_id') else []
            
        #     for user in vote_dict['user_id']:
        #         user['image'] = str(user['image']) if user.get('image') else ''
        #     response_data['vote'] = vote_dict
        # else:
        #     response_data['vote'] = {}
            
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            response_data
        )
    
    def edite_message(self, event):
        print("event",event)
        voting_question_id = event['voting_question']
        voting_question = Voting_Questions.objects.get(id=voting_question_id)
        self.send(text_data=json.dumps({
            'type': "edite_message_List_popel",
            'room_id':event['room_id'],
            'msg_id':event['msg_id'],
            'voting_question': {
                'id': voting_question.id,
                'question_text': voting_question.question,
                'list_of_people_who_vote': list(voting_question.list_of_people_who_vote.values_list('id', flat=True))
            }
        }, cls=DjangoJSONEncoder))
        
    def receive(self, text_data):
        print("text_data",text_data)
        try:
          text_data_json = json.loads(text_data)
          get_type=text_data_json.get('type' , '')
          room = text_data_json.get('room', '')
          
          if get_type == 'Eidet_questions':
                questions_id=text_data_json.get('questions_id' , '')
                UserFulterArry_id=text_data_json.get('UserFulterArry_id' , '')
                room_id=text_data_json.get('room_id' , '')
                msg_id=text_data_json.get('msg_id' , '')
                count = self.ADD_USER_TO_QUESTION(room_id , msg_id , room , questions_id , UserFulterArry_id )
          if get_type == 'chat_message':
            print("chat_message", get_type)

                
            message_in_user = text_data_json.get('message', '')
            # room_slug = text_data_json.get('room', '')
            image = text_data_json.get('image', None)
            room_obj = self.get_data_in_this_room(room)
            room_users = self.get_users_in_room(room_obj)
            other_users = self.get_other_users_in_room_only_first(room_obj)
            user_obj = self.get_data_user_join_naw(self.user_id)   # print(user_obj['user_name'])
            vote = text_data_json['vote']

            # print("vote" ,vote)
            message = self.handell_message(message_in_user)
            
            chat = self.save_chat(message ,image , room_obj , other_users , vote)
            # online_or_offline = self.handle_send_msg_or_navgaction(room_users , message , chat , user_obj)
            online_or_offline = True
            # filter_users = self.filter_users(room_obj , text_data_json)
            # print("room_usersroom_users" , room_users , "filter_users" , filter_users)
            # message_qs = Chat.objects.filter(room_id=room_obj, is_read=False)        
            # message_qs.update(is_read=True)
               
            # print("chat",chat)
            if online_or_offline:
                response_data = {
                    'type': 'chat.message',
                    'state':'chat_message',
                    'message': chat.message if hasattr(chat, 'message') else '',
                    'room_id': room_obj.id if hasattr(room_obj, 'id') else '',
                    # 'room_slug': room_obj.slug if hasattr(room_obj, 'slug') else '',
                    'created_at': chat.created_at if chat and chat.created_at else '',
                    'user_id': self.user_id,
                    'user_name': user_obj['user_name'],
                    'user_image': user_obj['image'] if user_obj['image'] else None,
                    'image': chat.image.url if chat and chat.image else None,
                    'room_users':room_users, # add this line to include the room users in the response
                    'is_read':chat.is_read if chat and hasattr(chat, 'is_read') else '',
                    # 'vote':chat.vote if chat and hasattr(chat, 'vote') else [],
                }
                if chat:
                    response_data['id'] = chat.id
            
                    if chat and hasattr(chat, 'vote'):
                        vote_dict = model_to_dict(chat.vote) if chat.vote else {}
                        vote_dict['files'] = str(vote_dict['files']) if vote_dict.get('files') else ''
                        vote_dict['image'] = str(vote_dict['image']) if vote_dict.get('image') else ''
                        voting_questions = vote_dict.get('voting_questions', [])
                        print("voting_questions",voting_questions)
                        
                        # voting_questions_data = []
                        # for question in voting_questions:
                        #     for key, value in question.items():
                        #         voting_questions_data.append(Voting_Questions.objects.create(vote=chat.vote, question=value))
                        vote_dict['voting_questions'] = [model_to_dict(question) for question in voting_questions]
                       
                        vote_dict['user_id'] = [model_to_dict(user) for user in vote_dict['user_id']] if vote_dict.get('user_id') else []
                       
                        for user in vote_dict['user_id']:
                            user['image'] = str(user['image']) if user.get('image') else ''
                        response_data['vote'] = vote_dict
                    else:
                        response_data['vote'] = {}
                                
                async_to_sync(self.channel_layer.group_send)(
                    self.room_group_name,
                    response_data
                )            
        except (ValueError, NewUser.DoesNotExist, Room.DoesNotExist) as e:
            print(f"An error occurred: {e}")
            self.send(text_data=json.dumps({'error': str(e)}))
            return
    
        except Exception as e:
            print(f"An error occurred in receive2: {e}")
            self.send(text_data=json.dumps({'error': "Something went wrong"}))
    
    
    
    def chat_message(self, event):
        # print("chat_message event125",event)
        try:
            if 'id' not in event:
                raise ValueError("'id' key is not present in event")
            if 'user_id' not in event:
                raise ValueError("'user_id' key is not present in event")
                        
            self.Send_message_to_WebSocket(event)
            # print(f"lllllllllllllllllllllllll" ,event )

    
        except KeyError as e:
            # Handle the KeyError exception
            print(f"KeyError occurred in chat_message: {e}")
            self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))
        except Chat.DoesNotExist as e:
            # Handle the DoesNotExist exception
            print(f"Chat.DoesNotExist occurred in chat_message: {e}")
            self.send(text_data=json.dumps({'error': 'Chat message does not exist.'}))
        except Exception as e:
            # Handle any other exception
            print(f"An error occurred in chat_message: {e}")
            self.send(text_data=json.dumps({'error': str(e)}))
    
    def Send_message_to_WebSocket(self , event):
            # print("send_message",event)
            # Send message to WebSocket     

            image_url = event.get('image', None)
            if image_url:
                image_url = settings.SITE_URL + image_url
            # vote = JSON.parse(event.vote);
            # print('is_readis_readis_read',event['is_read'])
            # Send message to WebSocket
            #'state':'edi
                
            self.send(text_data=json.dumps({
                'type': event['state'],
                'id': event['id'],
                'message': event['message'],
                'room_id': event['room_id'],
                'user_name': event['user_name'],
                'user_image': event['user_image'],
                'created_at': event['created_at'],
                'user_id': event['user_id'],
                'room_users': event['room_users'],
                'image': image_url,
                'is_read':event['is_read'],
                'vote':event['vote']
            }, cls=DjangoJSONEncoder))



    def update_user_chat_room_status(self, is_activeChat):
        try:
            # Check current user status
            current_status = NewUser.objects.filter(id=self.user_id, is_activeChat=is_activeChat).exists()
            
            # If current status is not equal to new status
            if not current_status:
                # Update user status
                NewUser.objects.filter(id=self.user_id).update(is_activeChat=is_activeChat)
                
        except Exception as e:
            # Handle any exceptions that might occur
            print(f"Error updating user status in update_user_chat_room_status: {str(e)}")
           


































































# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder

# import io
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from chat3.models import Room, Chat
# from users.models import NewUser
# import base64
# from datetime import datetime
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.conf import settings




# from channels.layers import get_channel_layer
# from django.dispatch import receiver
# from django.db.models.signals import post_save






# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
# import json
# import io
# import base64
# from datetime import datetime
# from .models import Chat, Room
# import uuid



# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
# import json
# import io
# import os
# import base64
# from datetime import datetime

# from .models import Chat, Room
# import uuid
# from urllib.parse import parse_qs
# import jwt
# from django.conf import settings




# def get_user(state):
#     return state

# class ChatConsumer(WebsocketConsumer):

#     def connect(self):
#         self.extract_user_info()
#         self.join_room_group()
#         self.accept()
    
    
        
#     def get_user_from_token(self , token):
#         try:
#             print("Got user from token")
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = payload.get('user_id')
#             user_name = payload.get('user_name')
#             email = payload.get('email')
#             is_online=payload.get('is_online')
#             return {'user_id': user_id, 'user_name': user_name, 'email': email , 'is_online':is_online}
#         except jwt.exceptions.DecodeError:
#             # Invalid token
#             return None
#         except jwt.exceptions.ExpiredSignatureError:
#             # Token has expired
#             return None
    
#     def extract_user_info(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
    
#         query_string = self.scope['query_string'].decode()
#         params = parse_qs(query_string)
#         token = params.get('token', [None])[0]
    
#         user = self.get_user_from_token(token)
#         if user is not None:
#             self.user_id = user['user_id']
#             self.user_name = user['user_name']
#             self.email = user['email']
#             self.is_online = user['is_online']
#             state = get_user(f'online {self.email}')
#             print(state,state ,state)
#         else:
#             self.user_id = None
#             self.user_name = 'Anonymous'
#             self.email = None
    
#     def join_room_group(self):
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
    


#     def disconnect(self, close_code):
#         # Leave room group
#         state = get_user("offline")
#         print(state , state, state, state)
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )

    
        
     
    
#     def receive(self, text_data):
#         try:
#             user = self.scope['user']
#             text_data_json = json.loads(text_data)
#             user_id = text_data_json.get('user', None)
#             message = text_data_json.get('message', '')
#             room = text_data_json.get('room', '')
#             try:
#                 room_obj = Room.objects.get(name=room)
#                 users_in_room = room_obj.users.all()
#                 print("Users in Room:", ", ".join([user.user_name for user in users_in_room]))
#                 users_list = [room_obj.user_name for room_obj in users_in_room]
#                 print("users_listusers_list" , users_list)

#             except Room.DoesNotExist:
#                 raise ValueError("Room does not exist")
    
#             user_obj = NewUser.objects.filter(id=user_id).first()
            
#             image = text_data_json.get('image', None)
#             if message and not image:
#                 chat = Chat.objects.create(room_id=room_obj, message=message)
#                 chat.user_id.set([user_id])
#                 print(chat, "chat message created")
#             elif image:
#                 chat = Chat.objects.filter(id=image).first()
#                 if not chat:
#                     raise ValueError("Chat does not exist with this image")
    
#             # getRoom =  self.room_name
#             # user = user_obj
#             # print("roooooooooooooooooooooooooooooom" ,  room_obj.users)
#             # print(room_obj.users, room_obj.name, room_obj.id)
    
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'id': chat.id,
#                     'user': user_id,
#                     'message': chat.message if hasattr(chat, 'message') else '',
#                     'room': chat.room_id.id if hasattr(chat, 'room_id') else '',
#                     'created_at': chat.created_at.replace(tzinfo=None).strftime('%H:%M:%S') if hasattr(chat, 'created_at') else '',
#                     'user_id': user_id,
#                     'user_name': user_obj.user_name,
#                     'user_image': user_obj.image.url if user_obj.image else None,
#                     'image': chat.image.url if chat.image else None,
#                     'room_users':users_list # add this line to include the room users in the response
#                 }
#             )
            
    
#         except (ValueError, NewUser.DoesNotExist, Room.DoesNotExist) as e:
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))
#             return
    
#         except Exception as e:
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': "Something went wrong"}))
    
    
    
    
#     def chat_message(self, event):
#         # print("chat_message event",event)
#         try:
#             if 'id' not in event:
#                 raise ValueError("'id' key is not present in event")
#             if 'user_id' not in event:
#                 raise ValueError("'user_id' key is not present in event")

#             message_id = event['id']
#             message = event['message']
#             room_id = event['room']
#             created_at = event['created_at']
#             user_id = event.get('user_id')
#             user_name = event['user_name']
#             user_image = event['user_image']
#             image_url = event['image']
#             created_at_string = '2023-03-02T16:23:37.790062+00:00'
#             created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
#             if image_url:
#                 image_url = settings.SITE_URL+image_url
#             if not image_url:
#                 image_url = None
                
            
#             print(room_id)
            
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({
#                 'type':"chat_message",
#                 'id': message_id,
#                 'message': message,
#                 'room_id': room_id,
#                 'image': image_url,
#                 # 'image': settings.SITE_URL + str(image_url),
#                 'user_image': user_image,
#                 'user_id': user_id,
#                 'user_name':user_name,
#                 # 'created_at': created_at,
#                 # 'created_time': created_at.strftime('%H:%M:%S'),
#                 'created_time': created_at.strftime('%H:%M:%S'), # format time only
#                 "state":"not_read"
#             }, cls=DjangoJSONEncoder))
   
#         except KeyError as e:
#             # Handle the KeyError exception
#             print(f"KeyError occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))
#         except Chat.DoesNotExist as e:
#             # Handle the DoesNotExist exception
#             print(f"Chat.DoesNotExist occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Chat message does not exist.'}))
#         except Exception as e:
#             # Handle any other exception
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
#     def send_message(self, event):
#         # print("send_message event", event)
#         try:
#             if 'id' not in event:
#                 raise ValueError("'id' key is not present in event")
#             if 'user_id' not in event:
#                 raise ValueError("'user_id' key is not present in event")

#             message_id = event['id']
#             message = event['message']
#             room_id = event['room']
#             created_at = event['created_at']
#             user_id = event.get('user_id')
#             user_name = event['user_name']
#             user_image = event['user_image']
#             image_url = event['image']
#             created_at_string = '2023-03-02T16:23:37.790062+00:00'
#             created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
#             # self.send_single_message(message_id, message, room_id, image_url, user_image, user_id, user_name, created_at)
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({
#                 'type': 'send_message',
#                 'id': message_id,
#                 'message': message,
#                 'room_id': room_id,
#                 'image': image_url,
#                 'user_image': user_image,
#                 'user_id': user_id,
#                 'user_name':user_name,
#                 # 'created_at': created_at,
#                 # 'created_time': created_at.strftime('%H:%M:%S'),
#                 'created_time': created_at.strftime('%H:%M:%S'), # format time only
#             }, cls=DjangoJSONEncoder))
#             print("message_id" , message_id)
            
   
#         except KeyError as e:
#             # Handle the KeyError exception
#             print(f"KeyError occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))
#         except Chat.DoesNotExist as e:
#             # Handle the DoesNotExist exception
#             print(f"Chat.DoesNotExist occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Chat message does not exist.'}))
#         except Exception as e:
#             # Handle any other exception
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))

    










    
    # def receive(self, text_data):
    #     # print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",text_data)
    #     try:
    #         user = self.scope['user']
    #         text_data_json = json.loads(text_data)
    #         user_id = text_data_json.get('user', None)
    #         message = text_data_json.get('message', '')
    #         room = text_data_json.get('room', '')
    #         try:
    #             room = Room.objects.get(name=room)
    #             room2 = Room.objects.filter(name=room).first() 
    #         except Room.DoesNotExist:
    #             raise ValueError("Room does not exist")
    
    #         user = NewUser.objects.filter(id=user_id).first()  # retrieve the actual NewUser object
    #         # Get image data, if any
    #         image = text_data_json.get('image', None)
    
    #         if message and not image:  # If the message does not have an image
    #             chat = Chat.objects.create(room_id=room, message=message)
    #             chat.user_id.set([user_id])
    #             print(chat, "chat message created")
    #         elif image:  # If the message has an image
    #             chat = Chat.objects.filter(id=image).first()
    #             if not chat:  # If no chat exists with this image
    #                 raise ValueError("Chat does not exist with this image")
            
    #         getRoom =  self.room_name
    #         user = user
    #         print("roooooooooooooooooooooooooooooom" ,  room2.users)
    #         print(room2.users, room2.name, room2.id)

    #         # print("is_onlineis_onlineis_onlineis_onlineis_online" ,  user.is_online)
    
    #         # Send message to room group
    #         async_to_sync(self.channel_layer.group_send)(
    #             self.room_group_name,
    #             {
    #                 'type': 'chat_message',
    #                 'id': chat.id,
    #                 'user': user_id,
    #                 'message': chat.message if hasattr(chat, 'message') else '',
    #                 'room': chat.room_id.id if hasattr(chat, 'room_id') else '',
    #                 'created_at': chat.created_at.replace(tzinfo=None).strftime('%H:%M:%S') if hasattr(chat, 'created_at') else '',
    #                 'user_id': user_id,
    #                 'user_name': user.user_name,
    #                 'user_image': user.image.url if user.image else None,
    #                 'image': chat.image.url if chat.image else None,
    #             }
    #         )
    
    #     except (ValueError, NewUser.DoesNotExist, Room.DoesNotExist) as e:
    #         # Handle the exception here
    #         print(f"An error occurred: {e}")
    #         self.send(text_data=json.dumps({'error': str(e)}))
    #         return
    
    #     except Exception as e:
    #         # Handle the exception here
    #         print(f"An error occurred: {e}")
    #         self.send(text_data=json.dumps({'error': "Something went wrong"}))
    



























# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder

# import io
# import json
# from asgiref.sync import async_to_sync
# from channels.generic.websocket import WebsocketConsumer
# from chat3.models import Room, Chat
# from users.models import NewUser
# import base64
# from datetime import datetime
# from channels.generic.websocket import AsyncWebsocketConsumer
# from django.conf import settings




# from channels.layers import get_channel_layer
# from django.dispatch import receiver
# from django.db.models.signals import post_save






# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
# import json
# import io
# import base64
# from datetime import datetime
# from .models import Chat, Room
# import uuid



# from channels.generic.websocket import WebsocketConsumer
# from asgiref.sync import async_to_sync
# from django.core.files.uploadedfile import InMemoryUploadedFile
# from django.core.serializers.json import DjangoJSONEncoder
# from django.conf import settings
# import json
# import io
# import os
# import base64
# from datetime import datetime

# from .models import Chat, Room
# import uuid
# from urllib.parse import parse_qs
# import jwt
# from django.conf import settings






# class ChatConsumer(WebsocketConsumer):

#     def connect(self):
#         self.extract_user_info()
#         self.join_room_group()
#         # self.initialize_sent_messages_list()
#         # query_params = parse_qs(self.scope['query_string'].decode('utf-8'))
#         # mssege_in_lockalhost = query_params.get('mssege_in_lockalhost', [''])[0]
#         # if mssege_in_lockalhost == "true":
#         #     self.send_old_messages_to_client()
#         #     # use mssege_in_lockalhost value in your code
#         #     print(f"mssege_in_lockalhost21: {mssege_in_lockalhost}")
#         self.accept()
    
    
        
#     def get_user_from_token(self , token):
#         try:
#             print("Got user from token")
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user_id = payload.get('user_id')
#             user_name = payload.get('user_name')
#             email = payload.get('email')
#             is_online=payload.get('is_online')
#             return {'user_id': user_id, 'user_name': user_name, 'email': email , 'is_online':is_online}
#         except jwt.exceptions.DecodeError:
#             # Invalid token
#             return None
#         except jwt.exceptions.ExpiredSignatureError:
#             # Token has expired
#             return None
    
#     def extract_user_info(self):
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = 'chat_%s' % self.room_name
    
#         query_string = self.scope['query_string'].decode()
#         params = parse_qs(query_string)
#         token = params.get('token', [None])[0]
    
#         user = self.get_user_from_token(token)
#         if user is not None:
#             self.user_id = user['user_id']
#             self.username = user['username']
#             self.email = user['email']
#             self.is_online = user['is_online']
#         else:
#             self.user_id = None
#             self.username = 'Anonymous'
#             self.email = None
    
#     def join_room_group(self):
#         async_to_sync(self.channel_layer.group_add)(
#             self.room_group_name,
#             self.channel_name
#         )
    
#     def initialize_sent_messages_list(self):
#         self.sent_messages = []
    
#     def send_old_messages_to_client(self):
#         old_messages = Chat.objects.filter(room_id__name=self.room_name).order_by('-id')
#         for message in old_messages:
#             if message.id not in self.sent_messages:
#                 self.send_chat_message_to_group(message)
    
#     def send_chat_message_to_group(self, message):
#         print('send_chat_message_to_group' , message)
#         async_to_sync(self.channel_layer.group_send)(
#             self.room_group_name,
#             {
#                 'type': 'chat_message',
#                 'id': message.id,
#                 'message': message.message,
#                 'room': message.room_id.id,
#                 'user': message.user_id,
#                 'user_id': [user.id for user in message.user_id.all()],
#                 'user_name': [user.user_name for user in message.user_id.all()],
#                 'image': message.image.url if message.image else None,
#                 'user_image': [user.image.url for user in message.user_id.all()],
#                 'created_at': message.created_at.replace(tzinfo=None).strftime('%H:%M:%S'),
#                 'site_url': settings.SITE_URL,
#                 'state_message': "new",
#             }
#         )
#         self.sent_messages.append(message.id)
    


#     def disconnect(self, close_code):
#         # Leave room group
#         async_to_sync(self.channel_layer.group_discard)(
#             self.room_group_name,
#             self.channel_name
#         )


    
 


#     def receive(self, text_data):
#         print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk",text_data)
#         try:
#             user = self.scope['user']
#             text_data_json = json.loads(text_data)
#             user_id = text_data_json.get('user', None)
#             message = text_data_json.get('message', '')
#             room = text_data_json.get('room', '')
#             try:
#                 room = Room.objects.get(name=room)
#             except Room.DoesNotExist:
#                 raise ValueError("Room does not exist")
    
#             user = NewUser.objects.filter(id=user_id).first()  # retrieve the actual NewUser object
#             # Get image data, if any
#             image = text_data_json.get('image', None)
    
#             if message and not image:  # If the message does not have an image
#                 chat = Chat.objects.create(room_id=room, message=message)
#                 chat.user_id.set([user_id])
#                 print(chat, "chat message created")
#             elif image:  # If the message has an image
#                 chat = Chat.objects.filter(id=image).first()
#                 if not chat:  # If no chat exists with this image
#                     raise ValueError("Chat does not exist with this image")
    
#             # Send message to room group
#             async_to_sync(self.channel_layer.group_send)(
#                 self.room_group_name,
#                 {
#                     'type': 'chat_message',
#                     'id': chat.id,
#                     'user': user_id,
#                     'message': chat.message if hasattr(chat, 'message') else '',
#                     'room': chat.room_id.id if hasattr(chat, 'room_id') else '',
#                     'created_at': chat.created_at.replace(tzinfo=None).strftime('%H:%M:%S') if hasattr(chat, 'created_at') else '',
#                     'user_id': user_id,
#                     'user_name': user.user_name,
#                     'user_image': user.image.url if user.image else None,
#                     'image': chat.image.url if chat.image else None,
#                 }
#             )
    
#         except (ValueError, NewUser.DoesNotExist, Room.DoesNotExist) as e:
#             # Handle the exception here
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))
#             return
    
#         except Exception as e:
#             # Handle the exception here
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': "Something went wrong"}))
    
    
    
#     def chat_message(self, event):
#         print("chat_message event",event)
#         try:
#             if 'id' not in event:
#                 raise ValueError("'id' key is not present in event")
#             if 'user_id' not in event:
#                 raise ValueError("'user_id' key is not present in event")

#             message_id = event['id']
#             message = event['message']
#             room_id = event['room']
#             created_at = event['created_at']
#             user_id = event.get('user_id')
#             user_name = event['user_name']
#             user_image = event['user_image']
#             image_url = event['image']
#             created_at_string = '2023-03-02T16:23:37.790062+00:00'
#             created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
            
#             if image_url:
#                 image_url = settings.SITE_URL+image_url
#             if not image_url:
#                 image_url = None
                
            
            
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({
#                 'type':"chat_message",
#                 'id': message_id,
#                 'message': message,
#                 'room': room_id,
#                 'image': image_url,
#                 # 'image': settings.SITE_URL + str(image_url),
#                 'user_image': user_image,
#                 'user_id': user_id,
#                 'user_name':user_name,
#                 # 'created_at': created_at,
#                 # 'created_time': created_at.strftime('%H:%M:%S'),
#                 'created_time': created_at.strftime('%H:%M:%S'), # format time only
#             }, cls=DjangoJSONEncoder))
   
#         except KeyError as e:
#             # Handle the KeyError exception
#             print(f"KeyError occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))
#         except Chat.DoesNotExist as e:
#             # Handle the DoesNotExist exception
#             print(f"Chat.DoesNotExist occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Chat message does not exist.'}))
#         except Exception as e:
#             # Handle any other exception
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))
  
  
  
  
  
#     def send_message(self, event):
#         # print("send_message event", event)
#         try:
#             if 'id' not in event:
#                 raise ValueError("'id' key is not present in event")
#             if 'user_id' not in event:
#                 raise ValueError("'user_id' key is not present in event")

#             message_id = event['id']
#             message = event['message']
#             room_id = event['room']
#             created_at = event['created_at']
#             user_id = event.get('user_id')
#             user_name = event['user_name']
#             user_image = event['user_image']
#             image_url = event['image']
#             created_at_string = '2023-03-02T16:23:37.790062+00:00'
#             created_at = datetime.strptime(created_at_string, '%Y-%m-%dT%H:%M:%S.%f%z')
#             # self.send_single_message(message_id, message, room_id, image_url, user_image, user_id, user_name, created_at)
#             # Send message to WebSocket
#             self.send(text_data=json.dumps({
#                 'type': 'send_message',
#                 'id': message_id,
#                 'message': message,
#                 'room': room_id,
#                 'image': image_url,
#                 'user_image': user_image,
#                 'user_id': user_id,
#                 'user_name':user_name,
#                 # 'created_at': created_at,
#                 # 'created_time': created_at.strftime('%H:%M:%S'),
#                 'created_time': created_at.strftime('%H:%M:%S'), # format time only
#             }, cls=DjangoJSONEncoder))
#             print("message_id" , message_id)
            
   
#         except KeyError as e:
#             # Handle the KeyError exception
#             print(f"KeyError occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Required key missing in the event data.'}))
#         except Chat.DoesNotExist as e:
#             # Handle the DoesNotExist exception
#             print(f"Chat.DoesNotExist occurred: {e}")
#             self.send(text_data=json.dumps({'error': 'Chat message does not exist.'}))
#         except Exception as e:
#             # Handle any other exception
#             print(f"An error occurred: {e}")
#             self.send(text_data=json.dumps({'error': str(e)}))

    




