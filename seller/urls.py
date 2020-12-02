from django.conf.urls import url, include
from seller.views import SellerRegisterView


urlpatterns = [
    url(r'^register', SellerRegisterView.as_view(), name='seller_registration'),
]
