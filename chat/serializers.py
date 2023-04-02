# chat/serializers.py


from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Chat
from datetime import datetime
from rest_framework import serializers


class ChatSerializer(ModelSerializer):
    user = SerializerMethodField("get_name")
    created_at = serializers.DateTimeField(format="%B %d, %Y") 
    created_at2 = serializers.DateTimeField(format="%H : %M") 
    
    class Meta:
        model = Chat
        fields = ("__all__")
    def get_name(self, obj):
        return obj.user.user_name
    
    

class ChatSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Chat

