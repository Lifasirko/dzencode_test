from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Comment
from .serializers import CommentSerializer
from .tasks import send_email_notification


class ParentCommentViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Comment.objects.filter(parent__isnull=True).order_by('-created_at')
    serializer_class = CommentSerializer

    def list(self, request, *args, **kwargs):
        cache_key = 'parent_comments'
        cached_comments = cache.get(cache_key)
        if cached_comments:
            return Response(cached_comments)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def retrieve(self, request, pk=None):
        """
        Отримання коментаря з дочірніми коментарями
        """
        try:
            # Отримуємо основний коментар
            comment = Comment.objects.get(pk=pk)

            def get_children(comment):
                """Рекурсивно отримуємо всі дочірні коментарі"""
                children = Comment.objects.filter(parent=comment)
                return [
                    {
                        **CommentSerializer(child).data,
                        "children": get_children(child)
                    }
                    for child in children
                ]

            # Основний коментар із дочірніми
            response_data = {
                **CommentSerializer(comment).data,
                "children": get_children(comment),
            }

            return Response(response_data)

        except Comment.DoesNotExist:
            return Response({"detail": "Коментар не знайдено."}, status=404)

    def perform_create(self, serializer):
        comment = serializer.save()

        send_email_notification.delay(
            email=comment.email,
            message=f"Hello,\n\nYour comment '{comment.text}' has been successfully posted on our website.\n\n"
                    f"Thank you for your participation!\n\nBest regards,\nSupport Team",
        )

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'comments',
            {
                'type': 'comment_message',
                'message': {
                    'id': comment.id,
                    'user_name': comment.user_name,
                    'email': comment.email,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'parent_id': comment.parent.id if comment.parent else None,
                }
            }
        )

    def list(self, request, *args, **kwargs):
        cache_key = 'comments_list'
        cached_comments = cache.get(cache_key)
        if cached_comments:
            return Response(cached_comments)

        response = super().list(request, *args, **kwargs)
        cache.set(cache_key, response.data, timeout=60 * 5)
        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        print(f"Login attempt: {request.data}")
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            print(f"Login failed: {response.data}")
        return response
