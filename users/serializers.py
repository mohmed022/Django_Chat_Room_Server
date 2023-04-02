from rest_framework import serializers
from users.models import NewUser , Follow_Models



class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    email = serializers.EmailField(required=True)
    user_name = serializers.CharField(required=True)
    # first_name = serializers.CharField(max_length=50, write_only=True)
    # LastName = serializers.CharField(max_length=50, write_only=True)
    # Nationality = serializers.CharField(max_length=20, write_only=True)
    password = serializers.CharField(min_length=8, write_only=True)
    # ,'first_name', 'LastName', 'Nationality',
    class Meta:
        model = NewUser
        
        fields = ('email',
                  'user_name', 
                  'password' ,
                  'gender', 
                  'first_name' ,
                  'LastName' ,
                  )
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance




class FultDataUserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(min_length=8, )
    class Meta:
        model = NewUser
        read_only_fields = ('password','email', 'user_name' , 'last_login' , 'is_superuser'   , 'user_permissions' , 'groups' ,)
        fields = ( '__all__')




class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow_Models
        fields = ("__all__")

# {
# "email":"mohmed@m.com",
# "user_name":"mohmed",
# "first_name":"mohmed",
# "LastName":"mohmed",
# "password":"mohmed"
# }












# from rest_framework import serializers
# from users.models import NewUser


# class CustomUserSerializer(serializers.ModelSerializer):
#     """
#     Currently unused in preference of the below.
#     """
#     email = serializers.EmailField(required=True)
#     user_name = serializers.CharField(required=True)
#     first_name = serializers.CharField(max_length=50, write_only=True)
#     LastName = serializers.CharField(max_length=50, write_only=True)
#     Nationality = serializers.CharField(max_length=20, write_only=True)
#     password = serializers.CharField(min_length=8, write_only=True)
    
#     class Meta:
#         model = NewUser
#         fields = ('email', 'user_name', 'password' ,'first_name', 'LastName', 'Nationality',)
#         extra_kwargs = {'password': {'write_only': True}}

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         # as long as the fields are the same, we can just use this
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance




# class FultDataUserSerializer(serializers.ModelSerializer):
#     # ProfileModel = ProfileSerializer(read_only=False)
#     # Subject = Subjects_MSerializer(read_only=True)
#     # Subject=ChoiceField(choices=())
#     # created = serializers.DateTimeField()
#     # Subject = Subjects_MSerializer()
#     # created_at = models.DateTimeField(auto_now_add=True)
#     # Subject = Subjects_MSerializer(source= 'title')

#     # Subject = serializers.PrimaryKeyRelatedField(source='user.email')
#     class Meta:
#         model = NewUser
#         # read_only_fields = ('email', 'user_name', 'password' ,'first_name', 'LastName',)
#         fields = ('email' , 'user_name' , 'first_name' )


#         # fields = ('id' , 'name' , 'description' ,'photo' , 'slug' , 'Subjects_V' , 'created_by_Russian')
#         # fields = ("id" , "Subjects_M", "created_by_Russian", "created_at", "video_link", "pdf_file_R", "name", "description", "photo", "is_active", "like", 'slug')
        








