from rest_framework import serializers
from .models import Blogs, Comments, Likes, Tags

class TagsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags       
        fields = ['name']

class BlogsSerializer(serializers.ModelSerializer):
    tags = TagsSerializer(required=False, many=True)

    class Meta:
        model = Blogs
        fields = ['id', 'user', 'title', 'content', 'tags', 'media_file', 'created_at', 'updated_at']

    def create(self, validated_data):
        _tags = validated_data.pop("tags", [])
        tag_list = []
        for tag in _tags:
            _tag, _ = Tags.objects.get_or_create(**tag)
            tag_list.append(_tag.pk)

        _blog = Blogs.objects.create(**validated_data)

        _blog.tags.set(tag_list)

        return _blog

    def update(self, instance, validated_data):
        _tags = validated_data.pop("tags", [])
        tag_list = []
        for tag in _tags:
            _tag, _ = Tags.objects.get_or_create(**tag)
            tag_list.append(_tag.pk)
        instance.tags.clear()
        instance.tags.set(tag_list)

        return super(BlogSerializer,
                     self).update(instance, validated_data)
                
class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = '__all__'

class LikesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Likes
        fields = '__all__'
