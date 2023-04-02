
# chat/models.py

from unittest.util import _MAX_LENGTH
from django_resized import ResizedImageField
from django.contrib.auth.models import User
from django.db import models

from django.conf import settings




class Room(models.Model):
    name = models.CharField(max_length=255, blank=False)
    password = models.CharField(max_length=255, blank=False)
    def __str__(self):
        return str(self.name)

class Chat(models.Model):
    rooms = models.ForeignKey(Room, on_delete=models.CASCADE, blank=False, related_name="rooms")
    users = models.ForeignKey(
    settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='chatUser')
    message = models.TextField(blank=True)
    image = ResizedImageField(force_format='WEBP', size=None,scale=0.5, quality=75, upload_to='images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_at2 = models.DateTimeField(auto_now_add=True,null=True)

    # def __str__(self):
    #     return str(self.room)
    
    
    


    
    
    
    