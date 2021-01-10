from django.db import models
from ecom_backend.utils import upload_image
from api.models import  User, City, Pincode, State
from django.contrib.postgres.fields import ArrayField
from django.utils.text import slugify

class SellerRole:
    RETAILER=1
    DISTRIBUTOR=2
    WHOLESELLER=3


SELLER_ROLE_CHOICES = [
    (SellerRole.RETAILER, 'Retailer'),
    (SellerRole.DISTRIBUTOR, 'Distributor'),
    (SellerRole.WHOLESELLER, 'Whole Seller')
]

class ShopCategory:
    ONLY_HOME_DELIVERY=1
    ONLY_PICK_UP=2
    BOTH=3


SHOP_CATEGORY_CHOICES = [
    (ShopCategory.ONLY_HOME_DELIVERY, 'Only Home Delivery'),
    (ShopCategory.ONLY_PICK_UP, 'Only Pick Up'),
    (ShopCategory.BOTH, 'Both')
]

class SellerDetail(models.Model):
    shop_name = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)

    gst = models.CharField(max_length=20, null=True, blank=True)
    pancard = models.FileField(
        verbose_name='Upload Pan Card',
        upload_to=upload_image,
        null=True, blank=True
    )
    adharcard = models.FileField(
        verbose_name='Upload Aadhar Card',
        upload_to=upload_image,
        null=True, blank=True
    )
    logo = models.FileField(
        verbose_name='Upload Shop Logo',
        upload_to=upload_image,
        null=True, blank=True
    )
    board = models.FileField(
        verbose_name='Upload Shop Board Picture',
        upload_to=upload_image,
        null=True, blank=True
    )
    role = models.IntegerField(choices=SELLER_ROLE_CHOICES, default=SellerRole.RETAILER)
    minimum_order = models.IntegerField(null=True, blank=True)
    category = models.IntegerField(choices=SHOP_CATEGORY_CHOICES, default=ShopCategory.BOTH)
    pincodes = models.CharField(max_length=256, null=True, blank=True)
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    bank_city = models.CharField(max_length=20, null=True, blank=True)
    branch = models.CharField(max_length=20, null=True, blank=True)
    account_holder = models.CharField(max_length=20, null=True, blank=True)
    account_number = models.CharField(max_length=20, null=True, blank=True)
    bank = models.CharField(max_length=20, null=True, blank=True)
    proof = models.FileField(
        verbose_name='Upload Document For Bank Proof',
        upload_to=upload_image,
        null=True, blank=True
    )

    def __str__(self):
        return str(self.shop_name)



class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    detail = models.ForeignKey(SellerDetail, on_delete=models.CASCADE, null=True)
    identifier = models.CharField(verbose_name="Seller Identifer", max_length=100, null=True, blank=True)

    def __str__(self):
        return str(self.identifier)

    def save(self, *args, **kwargs):
        shop_name = self.detail.shop_name + ' ' + self.detail.city + ' ' + self.detail.state + ' ' + self.detail.zip_code
        self.identifier = slugify(shop_name)
        super(Seller, self).save(*args, **kwargs) 

