from .models import UserProfile
from rest_framework import serializers

class ProfileSerializer(serializers.ModelSerializer):
    # owner = serializers.ReadOnlyField(source='user.user_name')
    class Meta:
        model=UserProfile
        fields='__all__'