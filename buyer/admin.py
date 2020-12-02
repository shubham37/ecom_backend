from django.contrib import admin
from buyer.models import UserAddress, Card, Buyer, BuyerWishlist

# Register your models here.
admin.site.register(UserAddress) 
admin.site.register(Card) 
admin.site.register(Buyer) 
admin.site.register(BuyerWishlist)