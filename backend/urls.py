from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.conf import settings
from django.conf.urls.static import static
from comments.views import CommentViewSet, ParentCommentViewSet

# Router for API endpoints
router = DefaultRouter()
router.register(r'comments', CommentViewSet, basename='comments')
router.register(r'parent-comments', ParentCommentViewSet, basename='parent-comments')

urlpatterns = [
    # Admin and API token routes
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Route for retrieving a specific comment
    path('api/comments/<int:pk>/', CommentViewSet.as_view({'get': 'retrieve'}), name='comment-detail'),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
