from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, SearchView, ShippingOptionViewSet, \
    CategoryViewSet, SubCategoryViewSet, PopularCategoryViewSet


productrouter = DefaultRouter()

urlpatterns = [
    url(r'^search/', SearchView.as_view(), name='product_search_view')
]

productrouter.register(r'products', ProductViewSet)
productrouter.register(r'shipping_option', ShippingOptionViewSet)
productrouter.register(r'category', CategoryViewSet)
productrouter.register(r'popular_category', PopularCategoryViewSet)
productrouter.register(r'sub_category', SubCategoryViewSet)


urlpatterns += productrouter.urls
