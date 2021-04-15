from django.urls import path
from .views import BlogsView, CommentsView, LikesView

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name = 'blogs'),
    path('comments/<str:pk>', CommentsView.as_view(), name = 'comments'),
    path('likes/<str:pk>', LikesView.as_view(), name = 'likes'),
]