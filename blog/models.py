from django.db import models
from ecom_backend.utils import upload_image


# Create your models here.
class BlogComment(models.Model):
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=20, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=1)
    date_comment = models.DateField(verbose_name='date of comment', auto_now_add=True)


    def __str__(self):
        return str(self.comment)


class BlogImages(models.Model):
    image = models.ImageField(
        verbose_name='Upload Blog Image',
        upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.image)

class BlogTags(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.title)


class Blog(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    author = models.CharField(max_length=20, null=True, blank=True)
    date_create = models.DateField(verbose_name='Date of Blog', auto_now_add=True)
    comment = models.ManyToManyField(BlogComment, blank=True)
    images = models.ForeignKey(BlogImages, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(BlogTags, blank=True)


    def __str__(self):
        return str(self.title)


