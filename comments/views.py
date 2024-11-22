from django.core.cache import cache
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer
from .tasks import send_email_notification


class CommentViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        comment = serializer.save()
        # Відправляємо email
        send_email_notification.delay(
            email=comment.email,
            message=f"Hello,\n"
                    f"\n"
                    f"Your comment {comment.text} has been successfully posted on our website.\n"
                    f"\n"
                    f"Thank you for your participation!\n"
                    f"\n"
                    f"Best regards,\n"
                    f"Support Team",
        )  # Викликаємо завдання Celery

    def list(self, request, *args, **kwargs):
        # Ключ для кешу
        cache_key = 'comments_list'
        # Перевіряємо, чи є дані в кеші
        cached_comments = cache.get(cache_key)
        if cached_comments:
            return Response(cached_comments)

        # Якщо в кеші немає, виконуємо запит до бази
        response = super().list(request, *args, **kwargs)
        # Зберігаємо результат у кеш
        cache.set(cache_key, response.data, timeout=60 * 5)  # Кеш на 5 хвилин
        return response
