from django.shortcuts import render
from django.contrib.sites.shortcuts import get_current_site
from blogs.models import Blogs, Comments, Likes, Tags
from blogs.serializers import BlogsSerializer, CommentsSerializer, LikesSerializer, TagsSerializer
from blogs.mixins import PaginationHandlerMixin, BaseFilterMixin
from blogs.path import file_path
from rest_framework import status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
import os, json

class BaseView(APIView, PaginationHandlerMixin, BaseFilterMixin):
    permission_classes  = [permissions.IsAuthenticated]
    pagination_class    = PageNumberPagination
    
    def post(self, request):
        absurl = get_current_site(request).domain 
        path = 'http://' + absurl + '/' + file_path(request)
        _tags = request.data['tags']
        tags = json.loads(_tags)

        serializers = self.serializer_class(data={**{'user':request.user.pk,
                                                    'media_file':path,
                                                    'title':request.data['title'],
                                                    'content':request.data['content'],
                                                    'tags':tags,
                                                    }})
        serializers.is_valid(raise_exception=True)
        serializers.save()

        _data = serializers.data

        return Response(serializers.data, status.HTTP_201_CREATED)
    
    def get(self, request):
        instance = self.model_class.objects.filter(user=request.user.pk)
        queryset_list = self.filter_queryset(instance)
        page = self.paginate_queryset(queryset_list)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        

        return Response(serializer.data, status=status.HTTP_200_OK)

class LikeCommentView(APIView):
    permission_classes  = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user = request.data
        
        blog = Blogs.objects.get(id=pk)
        serializers = self.serializer_class(data={**user, **{'user':request.user.pk,
                                                             'blog':blog.id}})
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response(serializers.data, status.HTTP_201_CREATED)
    
    def get(self, request, pk):
        instance = self.model_class.objects.filter(user=request.user.pk)
        serializer = self.serializer_class(instance=instance, many=True)
    
        return Response(serializer.data, status=status.HTTP_200_OK)

class BlogsView(BaseView):
    serializer_class   = BlogsSerializer
    model_class        = Blogs

class CommentsView(LikeCommentView):
    serializer_class    = CommentsSerializer
    model_class         = Comments

class LikesView(LikeCommentView):
    serializer_class    = LikesSerializer
    model_class         = Likes
