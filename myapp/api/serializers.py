from rest_framework import serializers
from myapp.models import Item, ChatMessage, Activity, UserProfile

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'created_at', 'created_by']
        read_only_fields = ['created_by', 'created_at']

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'user', 'message', 'timestamp']
        read_only_fields = ['user', 'timestamp']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'action', 'timestamp']
        read_only_fields = ['user', 'timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'bio', 'avatar']
        read_only_fields = ['user']