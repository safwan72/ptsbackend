from django.db import models
from decimal import Decimal
# Create your models here.


def upload_category(instance, filename):
    return "Category/{instance.name}/{instance.name}.png".format(instance=instance)

class Category(models.Model):
    name=models.CharField(max_length=150)
    picture=models.ImageField(upload_to=upload_category,blank=True,null=True)
    isActive=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name    
    class Meta:
        verbose_name_plural = "Category"
        db_table = "Category"
        
        
def upload_image(instance, filename):
    return "Dish/{instance.dish_name}/{instance.dish_name}.png".format(instance=instance)


class DishModel(models.Model):
    dish_name=models.CharField(max_length=150)
    dish_picture=models.ImageField(upload_to=upload_image,blank=True,null=True)
    dish_category=models.ManyToManyField(Category,blank=True)
    dish_description=models.TextField(blank=True)
    dish_ingredients=models.TextField(blank=True)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
    availability=models.BooleanField(default=False)
    featured=models.BooleanField(default=False)
    added_at=models.DateTimeField(auto_now_add=True)

    @property
    def new_price(self):
        return round(Decimal(self.price-(self.discount)),3) 
    

    def __str__(self):
        return self.dish_name

    class Meta:
        verbose_name_plural = "Dish"
        db_table = "Dish"
        
        
class Feedback(models.Model):
    phone = models.CharField(max_length=20, blank=True)
    message=models.TextField(blank=True)
    email=models.EmailField(blank=False)
    resolved=models.BooleanField(default=False)
    added_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "FeedBack  " +str(self.id)  