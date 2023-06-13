from django.dispatch.dispatcher import receiver
from django.shortcuts import render
from . import models, serializers
from rest_framework import mixins, viewsets, generics
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view


@api_view(['GET','POST'])
def Allusers(request):
    admins=models.Admin.objects.all()
    customers=models.Customer.objects.all()
    adminprofileSerializer=serializers.AdminProfileSerializer(admins,context={'request': request},many=True)
    customerprofileSerializer=serializers.CustomerProfileSerializer(customers,context={'request': request},many=True)
    return Response({'admins':adminprofileSerializer.data,"customers":customerprofileSerializer.data})

import shortuuid
s = shortuuid.ShortUUID(alphabet="0123456789")    
class AuthSerializerView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

class CustomAdminCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.CustomAdminCreateSerializer
    
    def post(self, request):
        admin=models.User.objects.create_superuser(
            email=request.data['email'],
            username=request.data['username'],
            password='saf12345',
        )
        if admin:
            adminProfile=models.Admin.objects.filter(
                user=admin)
            if adminProfile:
                adminProfile=adminProfile[0]
                adminProfile.full_name=request.data['full_name'],
                adminProfile.address=request.data['address'],
                adminProfile.phone=request.data['phone']
            adminProfile.save()
        return Response(True)    
            
            
class CustomCustomerCreateView(generics.CreateAPIView, generics.ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.CustomerProfileSerializer
    
    def post(self, request):
        customer=models.User.objects._create_user(
            email=request.data['email'],
            username=request.data['username'],
            password='saf12345',
        )
        if customer:
            customerProfile=models.Customer.objects.filter(
                user=customer)
            if customerProfile:
                customerProfile=customerProfile[0]
                customerProfile.full_name=request.data['full_name']
                customerProfile.address=request.data['address']
                customerProfile.phone=request.data['phone']
            customerProfile.save()
        return Response(True)                

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
    

class adminProfileUpdateView(generics.RetrieveUpdateAPIView):
    queryset = models.Admin.objects.all()
    serializer_class = serializers.AdminProfileSerializer
    lookup_field = "user__id"
    def put(self, request, *args, **kwargs):
        user=models.User.objects.get(id=kwargs['user__id'])
        admin=models.Admin.objects.filter(user=user)
        if admin:
            admin=admin[0]
            admin.full_name=request.data['full_name']
            admin.address=request.data['address']
            admin.phone=request.data['phone']
            if request.data['profile_pic']!='null':
                print('Uploaded Profile Picture') 
                admin.profile_pic=request.FILES['profile_pic']
            admin.save()
            adminserializer=serializers.AdminProfileSerializer(admin,context={'request': request})
        return Response(adminserializer.data)
    
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer