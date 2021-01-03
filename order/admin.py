from django.contrib import admin
from order.models import Order, OrderDetail, OrderReview

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(OrderReview)
