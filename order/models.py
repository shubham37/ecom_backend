from django.db import models
from api.models import User
from product.models import Product


# Create your models here.
class TrackStatus:
    ORDERED=1
    SHIPPED=2
    OFD=3
    DELIVERED=4


TRACK_STATUS_CHOICES = [
    (TrackStatus.ORDERED, 'Ordered'),
    (TrackStatus.SHIPPED, 'Shipped'),
    (TrackStatus.OFD, 'Out For Delivery'),
    (TrackStatus.DELIVERED, 'Delivered')
]


class OrderDetail(models.Model):

    # MRP, discount_price, discount_type, tax, shipping_price, payable_amount 
    price = models.JSONField(null=True)

    # at order time feature and value of product like color, size,
    features = models.JSONField(null=True)

    # name, mobile, pincode, locality, address, landmark, alternate_mobile, add_type
    shipping_address = models.JSONField(null=True)
    is_billing_same = models.BooleanField(default=True)
    billing_address = models.JSONField(null=True)

    # order date, est_delivery_date, shipping_date, delivery_date
    track_dates = models.JSONField(null=True)

    # max_return_date, return condition
    return_policy = models.JSONField(null=True)

    payment_option = models.JSONField(null=True)




class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    ordered_date = models.DateField(verbose_name='date joined', auto_now_add=True)
    is_return_available = models.BooleanField(default=True)
    is_cancel_available = models.BooleanField(default=True)
    track_status = models.IntegerField(choices=TRACK_STATUS_CHOICES, default=TrackStatus.ORDERED)
    comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(default=1)
    quantity = models.IntegerField(default=1)
    measurement_parameter = models.CharField(max_length=10)


