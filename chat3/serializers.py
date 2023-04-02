# chat/serializers.py

from rest_framework import serializers
from chat3.models import Room, Chat , Notification
from users.models import NewUser
# from users.serializers import FultDataUserSerializer

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        


class FultDataUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ("id", "user_name", "image", "is_online")


class RoomFulterSerializer(serializers.ModelSerializer):
    user_count = serializers.IntegerField(read_only=True)
    users = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "name", "users", "created_at", "updated_at", "user_count")

    def get_user_count(self, obj):
        return obj.users.count()

    def get_users(self, obj):
        if obj.users.count() == 1:
            # إذا كان هناك مستخدم واحد فقط، قم بإرجاع تفاصيل هذا المستخدم
            return FultDataUserSerializer(obj.users.first()).data
        elif obj.users.count() == 2:
            # إذا كان هناك مستخدمان، قم بإرجاع تفاصيل المستخدم الآخر فقط
            request_user = self.context.get('request').user
            other_user = obj.users.exclude(id=request_user.id).first()
            return FultDataUserSerializer(other_user).data
        else:
            # إلا، فقم بإرجاع تفاصيل كل المستخدمين
            return FultDataUserSerializer(obj.users.all(), many=True).data



            









from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.conf import settings

class ChatSerializer(ModelSerializer):
    user_name = SerializerMethodField("get_user_name")
    user_image = SerializerMethodField("get_user_image")
    user_id = SerializerMethodField("get_user_id")
    # created_at = serializers.DateTimeField(format="%B %d, %Y") 
    # created_at2 = serializers.DateTimeField(format="%H : %M") 
    
    class Meta:
        model = Chat
        fields = ("__all__")
    
    def get_user_id(self, obj):
        user = obj.user_id.first()  # Get the first user object from the queryset
        return user.id if user else ""
    
    def get_user_name(self, obj):
        user = obj.user_id.first()  # Get the first user object from the queryset
        return user.user_name if user else ""
    
    def get_user_image(self, obj):
        user = obj.user_id.first()  # Get the first user object from the queryset
        if user and user.image:
            return user.image.url
        else:
            return ""
    
    
    
class ChatAllSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    room = serializers.StringRelatedField()

    class Meta:
        model = Chat
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_created.user_name')
    user_image = serializers.ImageField(source='user_created.image')
    room_id = serializers.CharField(source='chat.room_id.id')
    room_name = serializers.CharField(source='chat.room_id.name')
    

    class Meta:
        model = Notification
        fields = ['id', "user", "chat", 'room_id', 'room_name', "message", "is_read", "created_at", 'user_name', 'user_image']
 
# class NotificationSerializer(serializers.ModelSerializer):
#     user_name = SerializerMethodField("get_user_name")
#     user_image = SerializerMethodField("get_user_image")

#     class Meta:
#         model = Notification
#         fields = '__all__'
        
    # def get_user_name(self, obj):
    #     user = obj.user_notification.first()  # Get the first user object from the queryset
    #     return user.user_name if user else ""
    
    # def get_user_image(self, obj):
    #     user = obj.user_notification.first()  # Get the first user object from the queryset
    #     if user and user.image:
    #         return user.image.url
    #     else:
    #         return ""




# user_name_to , user_id , user_name , user_image