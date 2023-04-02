
# # chat/models.py

from unittest.util import _MAX_LENGTH
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone

from django.core.cache import cache

# class Room(models.Model):
#     name = models.CharField(max_length=255)
#     users = models.ManyToManyField(
#         settings.AUTH_USER_MODEL,
#         related_name='rooms',
#         blank=True
#     )
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

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


class Room(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='rooms',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)

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
        }


        
def uplodChat (instance, filname):
    return '/%Y/%m/%d/'.join(['Chat' , str(instance.image.name), filname])







class Chat(models.Model):
    # room_id = ShortUUIDField()
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="room_id")
    # user_to= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, related_name="user_to")
    
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL)
    user_to = models.ManyToManyField(settings.AUTH_USER_MODEL , related_name="user_to")
    message = models.TextField(blank=True)
    image = models.ImageField(upload_to=uplodChat ,blank=True,null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True )
    created_at2 = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return str(self.id)
    
    # def is_user_online(room_obj,user_id):
    #     cache_key = f'online_users_{room_obj.name}'
    #     online_users = cache.get(cache_key)
    #     print("online_userslllllll",online_users)
    #     if online_users is None:
    #         online_users = room_obj.users.filter(last_login__gte=timezone.now()-timezone.timedelta(seconds=30)).values_list('id', flat=True)
    #         cache.set(cache_key, online_users)
    #     return user_id.filter(id__in=online_users).exists()

    
    
    


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