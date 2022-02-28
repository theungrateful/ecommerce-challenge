from django.db import models
from django.conf import settings
from product.models import Product

class Order(models.Model):
    PENDING_STATE = "p"
    COMPLETED_STATE = "c"

    ORDER_CHOICES = (
        (PENDING_STATE, "pending"),
        (COMPLETED_STATE, "completed")
        )
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="order", on_delete=models.CASCADE)
    order_number = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=2, choices=ORDER_CHOICES, default="p")
    is_paid = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def create_order(buyer, order_number, is_paid=False):
        order = Order()
        order.buyer = buyer
        order.order_number = order_number
        order.is_paid = is_paid
        order.save()
        return order
    
    def __str__(self):
        return self.order_number

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product = models.ForeignKey(Product, related_name="product_order", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    @staticmethod
    def create_order_item(order, product, quantity):
        order_item = OrderDetail()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.save()
        return order_item
    
    def __str__(self):
        return "{}".format(self.order)
