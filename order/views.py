from ast import Not
from datetime import datetime
from datetime import timedelta
import pytz

from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework import permissions, status, exceptions

from .serializers import (
    OrderDetailSerializer,
    OrderSerializer,
    OrderDetailBasicSerializer,
)
from .models import Order, OrderDetail
from .models import Product

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('buyer', 'order_items__product').all()
    serializer_class = OrderSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['status']

    def get_queryset(self):
        user = self.request.user
        return Order.objects.prefetch_related('buyer','order_items__product').filter(buyer=user)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        order_items = OrderDetail.objects.filter(order=instance.id).all()
        for item in order_items:
            product = Product.objects.filter(
                id=str(item.product)
            ).first()
            order_quantity = item.quantity
            product.stock += order_quantity
            product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()


class OrderDetailViewSet(viewsets.ModelViewSet):
    queryset = OrderDetail.objects.select_related('order', 'product').all()
    serializer_class = OrderDetailSerializer
    permission_classes = [
        permissions.IsAdminUser, permissions.IsAuthenticatedOrReadOnly, IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['order__status', 'product__name']


    def get_queryset(self):
        user = self.request.user
        return OrderDetail.objects.select_related('order__buyer', 'product').filter(order__buyer=user)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_quantity = serializer.validated_data['quantity']
        user = self.request.user

        product = Product.objects.filter(
            id=str(serializer.validated_data['product'])
        ).order_by('created').first()

        if product and product.stock >= order_quantity:
            actual_quantity = product.stock
            product.stock = actual_quantity - order_quantity
            
        else:
            raise exceptions.NotAcceptable("Quantity of this product is out.")

        try:
            order = Order.objects.get(buyer=user, status="p")
            order_time = order.date_time + timedelta(minutes=60)
            now = datetime.now()
            now = pytz.utc.localize(now)

            if order_time < now:
                order.status="x"
                order.save(update_fields=['status'])
                order = Order().create_order(buyer=user, status="p")
        except ObjectDoesNotExist:
            order = Order().create_order(buyer=user, status="p")

        orderdetail_serializer = self.get_queryset().filter(order=order)
        print(serializer.validated_data['product'])
        print(orderdetail_serializer)
        
        if orderdetail_serializer:
            for order_product in orderdetail_serializer:
                print(order_product.product)
                if serializer.validated_data['product'] == order_product.product:
                    raise exceptions.NotAcceptable("The product exists in the order.")

        else:
            product.save(update_fields=['stock'])
            serializer.save()
            order_item = OrderDetail().create_order_item(order, product, order_quantity)
            serializer = OrderDetailBasicSerializer(order_item)
            headers = self.get_success_headers(serializer.data)

            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        product = Product.objects.filter(
            id=str(instance.product)
        ).order_by('created').first()

        order_quantity = instance.quantity
        product.stock += order_quantity
        product.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        instance.delete()