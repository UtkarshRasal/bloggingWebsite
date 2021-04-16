from django.urls import path
from .views import BlogsView, CommentsView, LikesView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('blogs/', BlogsView.as_view(), name = 'blogs'),
    path('comments/<str:pk>', CommentsView.as_view(), name = 'comments'),
    path('likes/<str:pk>', LikesView.as_view(), name = 'likes'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)