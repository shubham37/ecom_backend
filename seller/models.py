from django.db import models
from ecom_backend.utils import upload_image
from api.models import  User, City, Pincode, State


class SellerPersonalDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    zip_code = models.ForeignKey(Pincode, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.address)


class SellerRole:
    RETAILER=1
    WHOLESELLER=2


SELLER_ROLE_CHOICES = [
    (SellerRole.RETAILER, 'Retailer'),
    (SellerRole.WHOLESELLER, 'Whole Seller')
]

class ShopCategory:
    CATEGORY1=1
    CATEGORY2=2


SHOP_CATEGORY_CHOICES = [
    (ShopCategory.CATEGORY1, 'Category1'),
    (ShopCategory.CATEGORY2, 'Category2')
]


class SellerBusinessDetail(models.Model):
    gst = models.CharField(max_length=20, null=True, blank=True)
    pancard = models.ImageField(
        verbose_name='Upload Pan Card',
        upload_to=upload_image,
        null=True, blank=True
    )
    adharCard = models.ImageField(
        verbose_name='Upload Aadhar Card',
        upload_to=upload_image,
        null=True, blank=True
    )
    logo = models.ImageField(
        verbose_name='Upload Shop Logo',
        upload_to=upload_image,
        null=True, blank=True
    )
    shop_board = models.ImageField(
        verbose_name='Upload Shop Board Picture',
        upload_to=upload_image,
        null=True, blank=True
    )
    role = models.IntegerField(choices=SELLER_ROLE_CHOICES, default=SellerRole.RETAILER)
    minimum_home_delivery = models.IntegerField(null=True, blank=True)
    shop_category = models.IntegerField(choices=SHOP_CATEGORY_CHOICES, default=ShopCategory.CATEGORY1)


class SellerBankDetail(models.Model):
    ifsc = models.CharField(max_length=20, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    branch = models.CharField(max_length=20 )
    acc_holder = models.CharField(max_length=20, null=True, blank=True)
    acc_number = models.CharField(max_length=20, null=True, blank=True)
    bank_name = models.CharField(max_length=20, null=True, blank=True)
    bank_proof = models.ImageField(
        verbose_name='Upload Document For Bank Proof',
        upload_to=upload_image,
        null=True, blank=True
    )

class Seller(models.Model):
    bank_detail = models.ForeignKey(SellerBankDetail, on_delete=models.CASCADE)
    business_detail = models.ForeignKey(SellerBusinessDetail, on_delete=models.CASCADE)
    personal_detail = models.ForeignKey(SellerPersonalDetail, on_delete=models.CASCADE)


