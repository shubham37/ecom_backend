from django.contrib import admin
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from api.views import LoginOTPView, RegisterOTPView, SubscribeView, CustomerQueryView, Login, \
    StateViewSet, CityViewSet, PincodeViewSet


router = DefaultRouter()

urlpatterns = [
    url(r'^login_otp/', LoginOTPView.as_view(), name='commom_otp'),
    url(r'^register_otp/', RegisterOTPView.as_view(), name='commom_otp'),
    url(r'^subscribe/', SubscribeView.as_view(), name='subscribe_news_letter'),
    url(r'^customer_query/', CustomerQueryView.as_view(), name='customer_query'),
    url(r'^login/', Login.as_view(), name='login'),
]


router.register(r'state', StateViewSet)
router.register(r'city', CityViewSet)
router.register(r'pincode', PincodeViewSet)


urlpatterns += router.urls