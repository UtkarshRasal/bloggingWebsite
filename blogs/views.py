from django.shortcuts import render
from blogs.models import Blogs, Comments, Likes
from blogs.serializers import BlogsSerializer, CommentsSerializer
from blogs.mixins import PaginationHandlerMixin
from rest_framework import status, permissions, exceptions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

class BlogsView(APIView, PaginationHandlerMixin):
    serializer_class   = BlogsSerializer
    model_class        = Blogs
    pagination_class   = PageNumberPagination
    permissions_class  = [permissions.IsAuthenticated] 

    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data={**user, **{'user':request.user.pk}})
        serializers.is_valid(raise_exception=True)
        serializers.save()

        return Response(serializers.data, status.HTTP_201_CREATED)
    
    def get(self, request):
        instance = self.model_class.objects.filter(user=request.user.pk)
        # queryset_list = self.filter_queryset(instance)

        page = self.paginate_queryset(instance)
        if page is not None:
            serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
        else:
            serializer = self.serializer_class(instance, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
