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
    password = serializers.CharField(min_length=8, write_only=True)
    # ,'first_name', 'LastName', 'Nationality',
    class Meta:
        model = NewUser
        
        fields = ('email',
                  'user_name', 
                  'password' ,
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
        read_only_fields = ('password','email', 'user_name' , 'last_login' , 'is_superuser' )
        fields = ( '__all__')




class FollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow_Models
        fields = ("__all__")








