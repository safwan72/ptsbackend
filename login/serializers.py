from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ("id","username", "email","password")
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        user = models.User.objects._create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user


class CustomerProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    profile_pic=serializers.SerializerMethodField()

    class Meta:
        model = models.Customer
        fields = ("id","user", "profile_pic","full_name","phone","address","date_joined")

    def get_profile_pic(self, obj):
        request = self.context.get('request')
        profile_pic = obj.profile_pic.url
        return request.build_absolute_uri(profile_pic)




        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        token['isAdmin']=user.is_staff
        return token