
# # chat/models.py

from unittest.util import _MAX_LENGTH
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
import os
from datetime import datetime
from django.core.cache import cache
from django.core.validators import FileExtensionValidator

def uplodRoom (instance, filname):
    return '/%Y/%m/%d/'.join(['Room' , str(instance.image.name), filname])

# class Room(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.CharField(max_length=500)
#     users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='rooms',
#         blank=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     last_login = models.DateTimeField(auto_now=True)
#     is_online = models.BooleanField(default=False)
#     image = models.ImageField(upload_to=uplodRoom ,blank=True,null=True)

#     def __str__(self):
#         return self.name

#     def as_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'users': self.users,
#             'created_at': self.created_at.timestamp(),
#             'updated_at': self.updated_at.timestamp(),
#             'user_count': self.users.count(),
#         }

from django.utils.text import slugify

class Room(models.Model):
    ADMINISTRATOR = 'administrator'
    CLUB_LEADER = 'club_leader'
    CLUB_COACHES = 'club_coaches'

    ROLE_CHOICES = [
        (ADMINISTRATOR, 'Administrator'),
        (CLUB_LEADER, 'Club leader'),
        (CLUB_COACHES, 'Club coaches (team captains)'),
    ]

    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='rooms',
        blank=True
    )
    
    administrator = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='administrator',
        blank=True
    )
        
    club_leader = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='club_leader',
        blank=True
    )
            
    club_coaches = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='club_coaches',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)
    image = models.ImageField(upload_to=uplodRoom ,blank=True,null=True)
    # role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=True)
    # administrator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='administrator_rooms', blank=True, null=True)
    # club_leader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_leader_rooms', blank=True, null=True)
    # club_coaches = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='club_coaches_rooms', blank=True, null=True)

    def __str__(self):
        return self.name

    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'users': self.users,
            'created_at': self.created_at.timestamp(),
            'updated_at': self.updated_at.timestamp(),
            'user_count': self.users.count(),
            'role': self.role,
            'administrator': self.administrator,
            'club_leader': self.club_leader,
            'club_coaches': self.club_coaches,
        }

        
def uplodChat (instance, filname):
    return '/%Y/%m/%d/'.join(['Chat' , str(instance.image.name), filname])







def uplodChat(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'uploads/%s/%s%s' % (datetime.now().strftime('%Y/%m/%d'), instance.id, ext)

def uplodvote(instance, filename):
    ext = os.path.splitext(filename)[1]
    return 'uploads/%s/%s%s' % (datetime.now().strftime('%Y/%m/%d'), instance.id, ext)

class Voting_Questions(models.Model):
    # vote = models.ForeignKey('vote', on_delete=models.CASCADE, related_name='questions')
    list_of_people_who_vote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='votes', blank=True, null=True)
    question = models.TextField()
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.question

class list_of_people_who_vote(models.Model):
    list_of_people = models.ForeignKey('vote', on_delete=models.CASCADE, related_name='list_of_people')
    value_question = models.TextField()

    def __str__(self):
        return self.value_question

class vote(models.Model):
    # Chat_id = models.ForeignKey('Chat', on_delete=models.CASCADE, blank=True, null=True ,related_name="Chat_id_in_vote")    
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL)
    discussion_topic = models.TextField(blank=True)
    description_discussion = models.TextField(blank=True)
    voting_questions = models.ManyToManyField(Voting_Questions , related_name='votes', blank=True, null=True )
    files = models.FileField(upload_to=uplodvote, validators=[FileExtensionValidator(allowed_extensions=['pdf', 'zip', 'doc', 'jpg', 'png'])], blank=True)
    image = models.ImageField(upload_to=uplodvote ,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True )

    def __str__(self):
        return str(self.id)

class Chat(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="room_id")
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL)
    user_to = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_to", blank=True, null=True)
    message = models.TextField(blank=True)
    image = models.ImageField(upload_to=uplodChat, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    created_at2 = models.DateTimeField(auto_now_add=True, null=True)
    vote = models.ForeignKey(vote, on_delete=models.CASCADE, blank=True, null=True, related_name="chat_votes")

    def __str__(self):
        return str(self.id)

    










class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_notification')
    user_created = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creater_notification')
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="room_id_Notification")
    chat = models.OneToOneField(Chat, on_delete=models.CASCADE, related_name='chat_notification')
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ['-created_at']




# class Chat(models.Model):
#     # room_id = ShortUUIDField()
#     room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="room_id")
#     user_id = models.ManyToManyField(settings.AUTH_USER_MODEL)
#     message = models.TextField(blank=True)
#     image = models.ImageField(upload_to=uplodChat ,blank=True,null=True)
#     created_at = models.DateTimeField(auto_now_add=True,null=True )
#     created_at2 = models.DateTimeField(auto_now_add=True,null=True)

#     def __str__(self):
#         return str(self.id)
    
#     def is_user_online(self,room_obj):
#         useronline = room_obj.users.filter(last_login__gte=timezone.now()-timezone.timedelta(seconds=30)).exists()
#         print(f"useronline is {useronline}")
#         print(f"self.room_id.users is {self.room_id}")
#         print("rom_idrom_idrom_idrom_idrom_id",room_obj)
        
#         return useronline
    
    
    


# class Chat(models.Model):
#     # room_id = ShortUUIDField()
#     room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="room_id")
#     user_id = models.ManyToManyField(settings.AUTH_USER_MODEL)
#     message = models.TextField(blank=True)
#     image = models.ImageField(upload_to=uplodChat ,blank=True,null=True)
#     created_at = models.DateTimeField(auto_now_add=True,null=True )
#     created_at2 = models.DateTimeField(auto_now_add=True,null=True)

#     def __str__(self):
#         return str(self.id)