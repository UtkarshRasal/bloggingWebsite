from rest_framework import serializers
from .models import Blogs, Comments, Likes

class BlogsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'created_at', 'updated_at']

class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'