from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from buyer.views import BuyerSignup, BuyerViewSet, BuyerAddressViewSet, \
    PaymentOptionViewSet, BuyerWishlistViewset


buyerrouter = DefaultRouter()

urlpatterns = [
    url(r'^buyer_signup/', BuyerSignup.as_view(), name='buyer_signup'),
]


buyerrouter.register(r'buyer_detail',  BuyerViewSet)
buyerrouter.register(r'buyer_address',  BuyerAddressViewSet)
buyerrouter.register(r'buyer_card',  PaymentOptionViewSet)
buyerrouter.register(r'buyer_wishlist',  BuyerWishlistViewset)

urlpatterns += buyerrouter.urls



