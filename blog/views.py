from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework import status 
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from api.permissions import CustomPermission
from blog.models import Blog, BlogComment
from blog.serializers import BlogSerializer, BlogCommentSerializer


class BlogViewSet(ViewSet):
    queryset = Blog.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BlogSerializer

    def get_object(self, id):
        blog = self.queryset.filter(id=id)
        return blog

    # blog list
    def list(self, request):
        if  self.queryset.exists():
            serialize = self.serializer_class(self.queryset.all(), many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Blogs Found."}, status=status.HTTP_200_OK)


    # blog by id
    def retrieve(self, request, pk=None):
        blog = self.get_object(pk)
        if  blog:
            serialize = self.serializer_class(blog.last())
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Blog Found."}, status=status.HTTP_200_OK)


    # blog search by tag or topic
    @action(detail=False, methods=['POST'])
    def search(self, request):
        query = request.data.get('text')
        blogs = self.queryset.filter(
            (
                Q(tags__title__icontains=query) |
                Q(title__icontains=query)
            )
        )
        if blogs.exists():
            serialize = self.serializer_class(blogs, many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Blog Found."}, status=status.HTTP_204_NO_CONTENT)


    # latest blogs
    @action(detail=False, methods=['GET'])
    def latest(self, request):
        blogs = self.queryset.order_by('date_create')
        if blogs.exists():
            serialize = self.serializer_class(blogs[:3], many=True)
            return Response(data=serialize.data, status=status.HTTP_200_OK)
        return Response(data={'detail': "No Blog Found."}, status=status.HTTP_200_OK)

    # top blogs Blog with High User Rating
    # def search(self, request):
    #     pass



class BlogCommentViewSet(ViewSet):
    queryset = BlogComment.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = BlogCommentSerializer

    def create(self, request):
        blog_comment_data = self.request.data.get('blog_comment_data')
        blog_id= self.request.data.get('blog_id')
        try:
            bc = BlogComment.objects.create(**blog_comment_data)
            blog = Blog.objects.get(id=blog_id)
            if blog:
                blog.comment.add(bc)
                blog.save()
                return Response(data={"detail": 'Blog COmment Saved'}, status=status.HTTP_200_OK)
            return Response(data={"detail": 'Blog COmment Not Saved'}, status=status.HTTP_200_OK)            
        except Exception as e:
            return Response(data={'detail': "No Blog Found."}, status=status.HTTP_200_OK)
