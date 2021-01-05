from django.conf.urls import url, include
from seller.views import SellerRegisterView, SellerStoreView, SellerByPincodeView

urlpatterns = [
    url(r'^register', SellerRegisterView.as_view(), name='seller_registration'),
    url(r'^by_pincode', SellerByPincodeView.as_view(), name='seller_list'),
    url(r'^store', SellerStoreView.as_view(), name='seller_store'),
]
