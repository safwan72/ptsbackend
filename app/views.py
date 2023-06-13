from django.shortcuts import render
import json
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser,IsAuthenticated,BasePermission

@api_view(['GET','POST'])
def AddFeedBack(request):
    phone=request.data['phone']
    message=request.data['message']
    email=request.data['email']
    if email!=None:
            feedback=models.Feedback.objects.create(
                phone=phone,message=message,email=email
            )
            if feedback:
                return Response({'response':True})
    return Response({'response':False})
            

@api_view(['GET'])
def CategoryViewFunctionDishes(request,pk):
        dishesarr=[]
        category=models.Category.objects.get(id=pk)
        dishes=models.DishModel.objects.filter(dish_category=category).all()
        if dishes:
            for dish in dishes:
                dishesarr.append(dish)
        serializer = serializers.DishModelSerializer(dishesarr, many=True,context={'request':request})
        categoryserializer=serializers.CategorySerializer(category,context={'request': request})        
        return Response({'dishes':serializer.data,'category':categoryserializer.data})
    
    
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

@api_view(['POST'])
def DishUpdateViewFunction(request,pk):  
    dish=models.DishModel.objects.filter(id=pk)
    dish_category=json.loads(request.data['dish_category'])
    availability=True if request.data['availability']==True else False
    featured=True if request.data['featured']==True else False
    if dish:
        dish=dish[0]
        dish.dish_name=request.data['dish_name']
        dish.price=int(request.data['price'])
        dish.discount=int(request.data['discount'])
        dish.availability=availability
        dish.featured=featured
        dish.dish_description=request.data['dish_description']
        dish.dish_ingredients=request.data['dish_ingredients']
        dish.save()       
        for i in dish_category:
            category=models.Category.objects.filter(name=i)
            if category:
                dish.dish_category.add(category[0])
                dish.save()
    dish.save()
    dishserializer=serializers.DishModelSerializer(dish,context={'request': request})        
    return Response(dishserializer.data)

@api_view(['POST'])
def CategoryUpdateViewFunction(request,pk):  
    category=models.Category.objects.filter(id=pk)
    isActive=True if request.data['isActive']==True else False
    if category:
        category=category[0]
        category.name=request.data['name']
        category.isActive=isActive
        category.save()       
    category.save()
    dishserializer=serializers.CategorySerializer(category,context={'request': request})        
    return Response(dishserializer.data)

import random

@api_view(['GET'])
def AllDishViewFunction(request,state):
    dish=models.DishModel.objects.all()
    if state==0:
            newdishes = list(models.DishModel.objects.all())
            newdishes = random.sample(newdishes, 9)
            dishserializer=serializers.DishModelSerializer(newdishes,many=True,context={'request': request})
    else:
        dishserializer=serializers.DishModelSerializer(dish,many=True,context={'request': request})
    return Response(dishserializer.data)

@api_view(['GET'])
def DishByPriceFunc(request,price):
    print("price",price)
    dishes=models.DishModel.objects.all()
    dishesarr=[]
    if dishes:
        for dish in dishes:
            if price > dish.new_price:
                print(dish.new_price)
                dishesarr.append(dish)
    dishserializer=serializers.DishModelSerializer(dishesarr,many=True,context={'request': request})
    return Response(dishserializer.data)

@api_view(['GET'])
def AllCategoryViewFunction(request):
    category=models.Category.objects.all()
    categoryserializer=serializers.CategorySerializer(category,many=True,context={'request': request})        
    return Response(categoryserializer.data)

@api_view(['GET'])
def AllFeedback(request):
    feedback=models.Feedback.objects.all()
    feedbackserializer=serializers.FeedBackSerializer(feedback,many=True,context={'request': request})        
    return Response(feedbackserializer.data)



class DishModelView(viewsets.ModelViewSet):
    queryset=models.DishModel.objects.all()
    serializer_class=serializers.DishModelSerializer
    
    def create(self, request):
        dish_category=json.loads(request.data['dish_category'])
        availability=True if request.data['availability']==True else False
        featured=True if request.data['featured']==True else False
        
        dish_new=models.DishModel.objects.create(
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






@api_view(['GET'])
def FeedbackById(request,pk):  
    feedback=models.Feedback.objects.filter(id=pk)
    # resolved=True if request.data['resolved']==True else False
    # if feedback:
    #     feedback=feedback[0]
    #     feedback.resolved=resolved
    #     feedback.save()
    # feedback.save()
    dishserializer=serializers.FeedBackSerializer(feedback,many=True,context={'request': request})        
    return Response(dishserializer.data)


@api_view(['POST'])
def EditFeedbackById(request,pk):  
    feedback=models.Feedback.objects.filter(id=pk)
    resolved=True if request.data['resolved']==True else False
    if feedback:
        feedback=feedback[0]
        feedback.resolved=resolved
        feedback.save()
    feedback.save()
    dishserializer=serializers.FeedBackSerializer(feedback,context={'request': request})        
    return Response(dishserializer.data)