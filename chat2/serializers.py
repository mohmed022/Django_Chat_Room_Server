from rest_framework import serializers
from .models import Room, Message


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'room', 'created_at']

    def to_representation(self, instance):
        """
        Converts message room field to return only room id instead of room object.
        """
        data = super().to_representation(instance)
        data['room'] = instance.room.id
        return data
