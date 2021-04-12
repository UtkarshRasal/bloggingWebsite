from django.urls import path
from .views import BlogsView

urlpatterns = [
    path('blogs/', BlogsView.as_view(), name = 'blogs'),
]