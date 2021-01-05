from django.db import models
from api.models import User
from product.models import Product
from django.contrib.postgres.fields.jsonb import JSONField


# Create your models here.
class TrackStatus:
    ORDERED='Ordered'
    SHIPPED='Shipped'
    OFD='Out For Delivery'
    DELIVERED='Delivered'


TRACK_STATUS_CHOICES = [
    (TrackStatus.ORDERED, 'Ordered'),
    (TrackStatus.SHIPPED, 'Shipped'),
    (TrackStatus.OFD, 'Out For Delivery'),
    (TrackStatus.DELIVERED, 'Delivered')
]


class OrderDetail(models.Model):

    # MRP, discount_price, discount_type, tax, shipping_price, payable_amount 
    price_detail = models.JSONField(null=True)
    products = models.JSONField(default=list, null=True, blank=True)

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

    payment_details = models.JSONField(null=True)


class OrderReview(models.Model):
    comment = models.TextField(max_length=200)
    rating = models.IntegerField(default=1)

    def __str__(self):
        return str(self.comment)[:10]


class Order(models.Model):
    buyer = models.ForeignKey(User, on_delete=models.CASCADE)
    orderId = models.CharField(verbose_name="Order Identifier", max_length=10, unique=True, null=True, blank=True)
    order_detail = models.ForeignKey(OrderDetail, on_delete=models.CASCADE)
    ordered_date = models.DateField(verbose_name='date joined', auto_now_add=True)
    total_amount = models.IntegerField(verbose_name="Sub Total", default=0)
    is_return_available = models.BooleanField(default=True)
    is_cancel_available = models.BooleanField(default=True)
    current_status = models.CharField(max_length=20, choices=TRACK_STATUS_CHOICES, default=TrackStatus.ORDERED)
    review = models.OneToOneField(OrderReview, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.orderId)


