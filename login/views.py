from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from . import models, serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view



class AuthSerializerView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer


class CustomerProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.Customer.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    lookup_field = "user__id"
    def put(self, request, *args, **kwargs):
        user=models.User.objects.get(id=kwargs['user__id'])
        customer=models.Customer.objects.filter(user=user)
        if customer:
            customer=customer[0]
            customer.full_name=request.data['full_name']
            customer.address=request.data['address']
            customer.phone=request.data['phone']
            if request.data['profile_pic']!='null':
                print('Uploaded Profile Picture') 
                customer.profile_pic=request.FILES['profile_pic']
            customer.save()
            customerserializer=serializers.CustomerProfileSerializer(customer,context={'request': request})
        return Response(customerserializer.data)
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer