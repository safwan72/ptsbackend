from django.shortcuts import render
from . import models,serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from app.models import DishModel
from django.shortcuts import render, get_object_or_404
import json
from login.models import Customer,User

    
    
class CartModelView(viewsets.ModelViewSet):
    queryset=models.Cart.objects.all()
    serializer_class=serializers.MyCartSerializer
    
    
    def create(self,request):
        user=request.data['user'] 
        user=User.objects.get(id=user)  
        customer=Customer.objects.get(user=user)
        product=request.data['product']
        dishes=DishModel.objects.filter(id=product)
        dish=dishes[0]
        cart=models.Cart.objects.get_or_create(
            user=customer,
            dish=dish,
            purchased=False
        )
        order=models.Order.objects.filter(
            user=customer,
            ordered=False,
        )
        if order.exists():
            order=order[0]
            if order.items.filter(dish=dish).exists():
                cart[0].quantity += 1
                cart[0].save()
                order.save()
            else:
                order.cart_items.add(cart[0])
                order.save()
        else:
            order=models.Order.objects.create(
                user=customer,
            ordered=False
            )
            order.cart_items.add(cart[0])
            order.save()    
        return Response({'message':'Product Added To Cart'})
    
@api_view(['GET','POST'])
def increase_dish(request,pk):
    dish = get_object_or_404(DishModel, pk=pk)
    user=get_object_or_404(User,id=request.data['id'])  
    customer = get_object_or_404(Customer, user=user)
    cart=models.Cart.objects.get_or_create(dish=dish,user=customer,purchased=False)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(dish=dish).exists():
            cart[0].quantity+=1
            cart[0].save()
            order.save()
        else:
            order.items.add(cart[0])
            order.save()
    else:
        order=models.Order.objects.create(user=customer,ordered=False)
        order.save()
        order.items.add(cart[0])
        order.save()
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})
@api_view(['PUT','GET'])
def add_coupon(request,pk):
    user=get_object_or_404(User,id=pk)  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    mycoupon=request.data['coupon']
    coupon=models.Coupon.objects.filter(code=mycoupon)
    if coupon.exists():
        coupon=coupon[0]
        if order.exists():
            order=order[0]
            order.coupon=coupon
            order.save()
        return Response({'coupon':True})        
    else:
        return Response({'coupon':'Check Your Coupon. It is invalid '})   
    
    
         
@api_view(['PUT','GET'])
def add_address(request,pk):
    user=get_object_or_404(User,id=pk)  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    address=request.data['address']    
    first_name=request.data['first_name']    
    last_name=request.data['last_name']    
    zip=request.data['zip']    
    city=request.data['city']    
    phone=request.data['phone']    
    
    if order.exists():
        order=order[0]
        shipping=models.ShippingAddress.objects.create(
                address=address,
                first_name=first_name,
                last_name=last_name,
                zip=zip,
                city=city,
                phone=phone,
            )
        order.shipping_address=shipping
        order.save()
        return Response(True)        
    else:
        return Response({'status':False})        
    
@api_view(['GET','POST'])
def my_cart(request,pk):
    user=get_object_or_404(User,id=pk)  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request})
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':[]})

    
@api_view(['GET','POST'])
def my_orders(request,pk):
    user=get_object_or_404(User,id=pk)  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=True)
    if order.exists():
        orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
        return Response({'order':orderserializer.data})
    else:
        return Response({'order':[]})
    
@api_view(['GET','POST'])
def all_orders(request):
    order=models.Order.objects.all()
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    
@api_view(['GET','POST'])
def order_by_id(request,pk):
    order=models.Order.objects.filter(id=pk)
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request},many=True)
    return Response(orderserializer.data)
    

    
@api_view(['GET','POST','PUT'])
def order_by_id_edit(request,pk):
    ordered=True if request.data['ordered']==True else False
    delivered=True if request.data['delivered']==True else False
    received=True if request.data['received']==True else False
    order=models.Order.objects.filter(id=pk)
    
    if order:
        order=order[0]
        order.order_status=request.data['order_status']
        order.delivered=delivered
        order.ordered=ordered
        order.received=received
        order.delivery_charge=request.data['delivery_charge']
        order.save()
    return Response({'status':True})
    
@api_view(['GET','POST'])
def checkout(request,pk):
    user=get_object_or_404(User,id=pk)  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        cart=models.Cart.objects.filter(user=customer,purchased=False)
        if cart:
            cart=cart[0]
        order.ordered=True
        cart.purchased=True
        cart.save()
        order.save()
    return Response({'status':'ok'})

@api_view(['GET','POST'])
def decrease_dish(request,pk):
    dish = get_object_or_404(DishModel, pk=pk)
    user=get_object_or_404(User,id=request.data['id'])  
    customer = get_object_or_404(Customer, user=user)
    order=models.Order.objects.filter(user=customer,ordered=False)
    if order.exists():
        order=order[0]
        if order.items.filter(dish=dish).exists():
            cart=models.Cart.objects.filter(dish=dish,user=customer,purchased=False)
            cart=cart[0]
            if cart.quantity>1:
                    cart.quantity-=1
                    cart.save()
            else:
                    order.items.remove(cart)
                    cart.delete()
                    cart.save()
                    order.save()      
    orderserializer=serializers.MyOrderSerializer(order,context={'request': request}) 
    return Response({'order':orderserializer.data})
