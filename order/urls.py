from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from order.views import OrderPlaceView, OrderViewSet, PaymentBack

orderrouter = DefaultRouter()

urlpatterns = [
    url(r'^order_place', OrderPlaceView.as_view(), name='order_place_view'),
    url(r'^payment', PaymentBack.as_view(), name='payment_back')
]

orderrouter.register(r'orders', OrderViewSet)
# productrouter.register(r'shipping_option', ShippingOptionViewSet)


urlpatterns += orderrouter.urls
