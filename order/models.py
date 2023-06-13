from django.db import models
from login.models import Customer
from app.models import DishModel
from decimal import Decimal

# Create your models here.

class Cart(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,related_name='orderer')
    dish=models.ForeignKey(DishModel,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    purchased=models.BooleanField(default=False)
    added_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'{self.dish.dish_name} X {self.quantity}'
    
    @property
    def dish_total(self):
        price=self.dish.new_price*self.quantity          
        return round(Decimal(price),3) 
    
    class Meta:
        ordering=['-added_time',]
        verbose_name_plural='Cart'
    
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()

    def __str__(self):
        return self.code
    
STATUS_CHOICES = (
    ('UnConfirmed', 'UnConfirmed'),
    ('Confirmed', 'Confirmed'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Receieved', 'Receieved'),
)


class ShippingAddress(models.Model):
    address = models.TextField(blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zip = models.CharField(max_length=100)
    phone = models.CharField(max_length=100,null=True)
    city = models.CharField(max_length=100)
    def __str__(self):
        return f'{self.first_name}\'s X  Shipping Address'
    
    class Meta:
        verbose_name_plural = "Shipping Address"
        db_table = "Shipping Address"


class Order(models.Model):
    user = models.ForeignKey(Customer,on_delete=models.CASCADE)
    items = models.ManyToManyField(Cart)
    ordered = models.BooleanField(default=False)
    order_status = models.CharField(choices=STATUS_CHOICES,default=STATUS_CHOICES[0][0],max_length=20)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, blank=True, null=True)
    delivery_charge=models.IntegerField(default=50)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'{self.user.user.username}\'s X  Order'
    @property
    def total_price(self):
        total=0
        for i in self.items.all():
           total+=float(i.dish_total)
        total=total+self.delivery_charge
        return total 
    @property
    def total_price_after_discount(self):
        total=0
        for i in self.items.all():
           total+=float(i.dish_total)
        total=total+self.delivery_charge
        if self.coupon is not None:
            total=total-self.coupon.amount
        return total 

   