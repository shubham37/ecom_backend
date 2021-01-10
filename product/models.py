from django.db import models
from seller.models import Seller
from api.models import User
from ecom_backend.utils import upload_image


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=50)
    banner = models.ImageField(
        verbose_name='Upload Category Image',
        upload_to=upload_image,
        null=True, blank=True
    )
    is_top_category = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class PopularCategory(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_title = models.CharField(max_length=20, null=True, blank=True)
    banner = models.ImageField(
        verbose_name='Upload Category Image',
        upload_to=upload_image,
        null=True, blank=True
    )
    redirection = models.URLField(verbose_name='Redirect To', null=True, blank=True)

    def __str__(self):
        return self.sub_title

class SubCategory(models.Model):
    cat = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ProductImages(models.Model):
    image = models.ImageField(
        verbose_name='Upload Blog Image',
        upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.image)

class ShippingOptionGroup(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class ShippingOptions(models.Model):
    shipping_option_group = models.ForeignKey(ShippingOptionGroup, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class AllFeature(models.Model):
    key = models.CharField(max_length=20, verbose_name="Feature Key")

    def __str__(self):
        return str(self.key)

class FilterFeature(models.Model):
    feature = models.ForeignKey(AllFeature, on_delete=models.DO_NOTHING, null=True)
    is_filter = models.BooleanField(default=False, verbose_name='Is Available For Filter')

    def __str__(self):
        return str(self.feature)


class Feature(models.Model):
    name = models.CharField(max_length=20, verbose_name="Feature Name")
    value = models.CharField(max_length=20, verbose_name="Feature Value")

    def __str__(self):
        return str(self.name) + ' -- ' + str(self.value)

    def save(self, *args, **kwargs):
        if not AllFeature.objects.filter(key__iexact=self.name).exists():
            filters = AllFeature.objects.create(key=self.name)
        super(Feature, self).save(*args, **kwargs) 

class Product(models.Model):
    title = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, null=True, blank=True)
    date_added = models.DateField(verbose_name='date of product Add', auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, null=True, blank=True)
    images = models.ManyToManyField(ProductImages, blank=True)
    thumbnail = models.ForeignKey(ProductImages, related_name='thumb', null=True, blank=True, on_delete=models.CASCADE)
    mrp = models.IntegerField(default=100)
    quantity = models.IntegerField(default=1)
    unit = models.CharField(max_length=10, default=None, null=True, blank=True)
    view_count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.title)

class FeatureGroup(models.Model):
    title = models.CharField(verbose_name="Group Identifier", max_length=50)
    features = models.ManyToManyField(Feature, related_name='features')
    products = models.ManyToManyField(Product, related_name='product_features')

    def  __str__(self):
        return str(self.title)

class DiscountType:
    FLAT='FLAT'
    PERCENTAGE='PERCENTAGE'


DISCOUNT_TYPE_CHOICES = [
    (DiscountType.FLAT, 'FLAT'),
    (DiscountType.PERCENTAGE, 'PERCENTAGE'),
]

class DiscountGroup(models.Model):
    title = models.CharField(max_length=20, verbose_name='Title')
    discount_amount = models.IntegerField(verbose_name='Amount')
    discount_type = models.CharField(max_length=15, choices=DISCOUNT_TYPE_CHOICES, default=DiscountType.FLAT, verbose_name='Discount Type')
    products = models.ManyToManyField(Product, related_name='discount_group')

    def __str__(self):
        return str(self.title)

class ProductComment(models.Model):
    name = models.CharField(max_length=20, default=None, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)
    date_comment = models.DateField(verbose_name='date of comment', auto_now_add=True)

    def __str__(self):
        return str(self.comment)[:10]

