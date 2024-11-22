from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user_name', 'email', 'home_page', 'text', 'created_at', 'parent']
        read_only_fields = ['id', 'created_at']
