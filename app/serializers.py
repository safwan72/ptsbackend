from rest_framework import serializers
from . import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Category
        fields='__all__'
        depth=1

class FeedBackSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.Feedback
        fields='__all__'
        depth=1
        
class DishModelSerializer(serializers.ModelSerializer):
    dish_category=CategorySerializer(many=True,required=False)
    dish_picture=serializers.SerializerMethodField()
    new_price=serializers.SerializerMethodField()
    class Meta:
        model=models.DishModel
        fields='__all__'
        depth=1
    def get_new_price(self, obj):
        return obj.new_price

    def get_dish_picture(self, obj):
        request = self.context.get('request')
        dish_picture = obj.dish_picture.url
        return request.build_absolute_uri(dish_picture)