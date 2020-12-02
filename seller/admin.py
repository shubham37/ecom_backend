from django.contrib import admin
from seller.models import SellerPersonalDetail, SellerBankDetail, SellerBusinessDetail, Seller

# Register your models here.
admin.site.register(SellerPersonalDetail) 
admin.site.register(SellerBankDetail) 
admin.site.register(SellerBusinessDetail) 
admin.site.register(Seller)