from django.contrib import admin
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('api.urls')),
    url(r'^blog_api/', include('blog.urls')),
    url(r'^buyer_api/', include('buyer.urls')),
    url(r'^order_api/', include('order.urls')),
    url(r'^product_api/', include('product.urls')),
    url(r'^seller_api/', include('seller.urls')),    
]

urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+= static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
