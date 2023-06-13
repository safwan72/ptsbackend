from django.views.decorators.csrf import requires_csrf_token
from rest_framework import serializers
from . import models
from login.serializers import CustomerProfileSerializer

class MyCouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coupon
        fields = "__all__"
        depth=1
        
class MyShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShippingAddress
        fields = "__all__"
        depth=1
        

class MyCartSerializer(serializers.ModelSerializer):
    user=CustomerProfileSerializer(required=False)
    dish_total=serializers.SerializerMethodField()
    class Meta:
        model = models.Cart
        fields = "__all__"
        depth=1
        
    def get_dish_total(self, obj):
        return obj.dish_total




class MyOrderSerializer(serializers.ModelSerializer):
    user=CustomerProfileSerializer(required=False)
    items=MyCartSerializer(many=True,required=False)
    total_price=serializers.SerializerMethodField()
    total_price_after_discount=serializers.SerializerMethodField()
    coupon=MyCouponSerializer(required=False)
    class Meta:
        model = models.Order
        fields = "__all__"
        depth=1
    def get_total_price(self, obj):
        return obj.total_price
    def get_total_price_after_discount(self, obj):
        return obj.total_price_after_discount


