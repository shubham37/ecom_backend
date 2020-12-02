from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from blog.views import BlogViewSet, BlogCommentViewSet


blogrouter = DefaultRouter()

urlpatterns = []

blogrouter.register(r'blogs', BlogViewSet)
blogrouter.register(r'blogs_comment', BlogCommentViewSet)

urlpatterns += blogrouter.urls
