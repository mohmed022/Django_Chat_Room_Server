from rest_framework import serializers
from chat3.models import Room, Chat , Voting_Questions, vote ,  Notification
from users.models import NewUser

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'
        

# class RoomFulterSerializer(serializers.ModelSerializer):
#     user_count = serializers.IntegerField(read_only=True)
#     users = serializers.SerializerMethodField()

#     class Meta:
#         model = Room
#         fields = ("id", "name", "description" ,"image", "users", "created_at", "updated_at",
#                   "user_count" , "club_coaches" , "club_leader" , "administrator")

#     def get_user_count(self, obj):
#         return obj.users.count()

    # def get_users(self, obj):
    #     users = obj.users.all()
    #     if users.exists():
    #         return FultDataUserSerializer(users, many=True).data
    #     else:
    #         return []

class FultDataUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ("id", "user_name", "image", "is_online")





class RoomFulterSerializer(serializers.ModelSerializer):
    user_count = serializers.IntegerField(read_only=True)
    users = serializers.SerializerMethodField()
    administrator = serializers.SerializerMethodField()
    club_coaches = serializers.SerializerMethodField()
    club_leader = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ("id", "name", "description" ,"image", "users", "created_at", "updated_at",
                  "user_count", "club_coaches", "club_leader", "administrator")

    def get_user_count(self, obj):        
        return obj.users.count()

    def get_users(self, obj):        
        users = set()
        if obj.administrator:
            users.add(obj.administrator)
        if obj.club_leader:
            users.add(obj.club_leader)
        if obj.club_coaches:
            users.add(obj.club_coaches)
        if obj.users.exists():
            users.update(obj.users.all())
        if users:
            return FultDataUserSerializer(users, many=True).data
        else:
            return []
        
    def get_administrator(self, obj):
        users = obj.administrator.all()
        if users.exists():
            return FultDataUserSerializer(users, many=True).data
        else:
            return []
        
    def get_club_coaches(self, obj):
        users = obj.club_coaches.all()
        if users.exists():
            return FultDataUserSerializer(users, many=True).data
        else:
            return []
        
    def get_club_leader(self, obj):
        users = obj.club_leader.all()
        if users.exists():
            return FultDataUserSerializer(users, many=True).data
        else:
            return []

       

     









from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ('id', 'first_name' , 'LastName' , 'is_staff')

class VotingQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting_Questions
        fields = '__all__'
        
class VoteSerializer(ModelSerializer):
    user_id = UserSerializer(many=True)
    voting_questions = VotingQuestionsSerializer(many=True)

    class Meta:
        model = vote
        fields = '__all__'
        

        
class ChatSerializer(ModelSerializer):
    user_name = SerializerMethodField("get_user_name")
    user_image = SerializerMethodField("get_user_image")
    user_id = SerializerMethodField("get_user_id")
    vote = VoteSerializer()
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





class Voting_QuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voting_Questions
        fields = ('id', 'question')

class voteSerializer(serializers.ModelSerializer):
    voting_questions = Voting_QuestionsSerializer(many=True)
    list_of_people_who_vote = serializers.SlugRelatedField(many=True, slug_field='username', queryset=NewUser.objects.all())

    class Meta:
        model = vote
        fields = ('id', 'Chat_id', 'user_id', 'discussion_topic', 'description_discussion', 'voting_questions', 'files', 'list_of_people_who_vote', 'image', 'created_at')






class NotificationSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user_created.user_name')
    user_image = serializers.ImageField(source='user_created.image')
    room_id = serializers.CharField(source='chat.room_id.id')
    room_name = serializers.CharField(source='chat.room_id.name')
    

    class Meta:
        model = Notification
        fields = ['id', "user", "chat", 'room_id', 'room_name', "message", "is_read", "created_at", 'user_name', 'user_image']
 