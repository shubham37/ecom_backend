from django.contrib import admin
from blog.models import BlogComment, BlogImages, BlogTags, Blog

# Register your models here.
admin.site.register(BlogComment) 
admin.site.register(BlogImages) 
admin.site.register(BlogTags) 
admin.site.register(Blog)