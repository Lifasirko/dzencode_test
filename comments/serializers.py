from rest_framework import serializers

from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id', 'user_name', 'email', 'home_page', 'text',
            'parent', 'created_at', 'image', 'text_file'
        ]
