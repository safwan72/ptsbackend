from django.shortcuts import render
import json
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission


@api_view(['GET'])
def CategoryViewFunctionDishes(request,pk):
        dishesarr=[]
        category=models.Category.objects.get(id=pk)
        dishes=models.DishModel.objects.filter(dish_category=category).all()
        if dishes:
            for dish in dishes:
                dishesarr.append(dish)
        serializer = serializers.DishModelSerializer(dishesarr, many=True,context={'request':request})
        return Response(serializer.data)
    
    
class CategoryCreateView(generics.ListCreateAPIView):
    queryset=models.Category.objects.all()
    serializer_class=serializers.CategorySerializer
    def create(self, request,*args,**kwargs):
        if request.data['picture'] and request.data['name']!='':
            name=request.data['name']
            picture=request.data['picture']
            isactive=True if request.data['isActive']=='true'  else False
        if name!=None and request.data['picture']:
            category=models.Category.objects.create(
                name=name,picture=picture,isActive=isactive
            )
            categoryserializer=serializers.CategorySerializer(category)
            return Response({'category':categoryserializer.data})
        else:
            return Response({'category':'False'})
        
        
@api_view(['GET'])
def DishViewFunction(request,pk):  
    dish=models.DishModel.objects.filter(id=pk)
    if dish:
        dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)


@api_view(['GET'])
def AllDishViewFunction(request):
    dish=models.DishModel.objects.all()
    dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)



class DishModelView(viewsets.ModelViewSet):
    queryset=models.DishModel.objects.all()
    serializer_class=serializers.DishModelSerializer
    
    def create(self, request):
        dish_category=json.loads(request.data['dish_category'])
        availability=True if request.data['availability']=='true' else False
        featured=True if request.data['featured']=='true' else False
        
        dish_new,created=models.DishModel.objects.get_or_create(
            dish_name=request.data['dish_name'],
            dish_picture=request.data['dish_picture'],
            price=request.data['price'],
            discount=request.data['discount'],
            availability=availability,
            featured=featured,
            dish_description=request.data['dish_description'],
            dish_ingredients=request.data['dish_ingredients'],
        )
        for i in dish_category:
            category=models.Category.objects.filter(name=i)
            if category:
                dish_new.dish_category.add(category[0])
                dish_new.save()
        dish_new.save()
        return Response({'message':'Added'})      
    
    
@api_view(['GET'])
def FeaturedDishesView(request):
    dish=models.DishModel.objects.filter(featured=True)
    dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})        
    return Response(dishserializer.data)