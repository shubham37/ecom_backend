from rest_framework import  serializers
from blog.models import Blog, BlogComment


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        depth = 1


class BlogCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogComment
        fields = '__all__'
