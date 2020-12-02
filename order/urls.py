from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from order.views import OrderPlaceView, OrderViewSet

orderrouter = DefaultRouter()

urlpatterns = [
    url(r'^order_place', OrderPlaceView.as_view(), name='order_place_view')
]

orderrouter.register(r'orders', OrderViewSet)
# productrouter.register(r'shipping_option', ShippingOptionViewSet)


urlpatterns += orderrouter.urls
