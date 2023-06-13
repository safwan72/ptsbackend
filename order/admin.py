from django.contrib import admin
from . import models
# Register your models here.

admin.site.register([models.Cart,models.Coupon,models.Order,models.ShippingAddress])