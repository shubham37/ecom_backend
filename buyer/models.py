from django.db import models
from api.models import User, State, City, Pincode
from product.models  import Product

# Create your models here.


class Gender:
    MALE=1
    FEMALE=2
    OTHER=3


GENDER_CHOICES = [
    (Gender.MALE, 'Male'),
    (Gender.FEMALE, 'Female'),
    (Gender.OTHER, 'Other')
]

class AddressType:
    HOME=1
    WORK=2
    OTHER=3


ADDRESS_TYPE_CHOICES = [
    (AddressType.HOME, 'Home'),
    (AddressType.WORK, 'Work'),
    (AddressType.OTHER, 'Other')
]


class UserAddress(models.Model):
    full_name = models.CharField(max_length=20, null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    pincode = models.ForeignKey(Pincode, on_delete=models.CASCADE)
    locality = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=20, null=True, blank=True)
    landmark = models.CharField(max_length=20, null=True, blank=True)
    alternative_mobile = models.CharField(max_length=20, null=True, blank=True)
    date_address = models.DateField(verbose_name='date of addres', auto_now_add=True)
    add_type = models.IntegerField(choices=ADDRESS_TYPE_CHOICES, default=AddressType.HOME)
    
    def __str__(self):
        return str(self.full_name)


class Card(models.Model):
    card_name = models.CharField(max_length=20, null=True, blank=True)
    number = models.CharField(max_length=20, null=True, blank=True)
    month = models.CharField(max_length=20, null=True, blank=True)
    year = models.CharField(max_length=20, null=True, blank=True)
    
    def __str__(self):
        return str(self.number)


class Buyer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    gender = models.IntegerField(default=0)
    date_joined = models.DateField(verbose_name='User Joined', auto_now_add=True)
    addresses = models.ManyToManyField(UserAddress, blank=True)
    cards = models.ManyToManyField(Card, blank=True)
    is_seller = models.BooleanField(default=False)

    def __str__(self):
        return str(self.first_name)


class BuyerWishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

