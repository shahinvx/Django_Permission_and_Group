from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import ProfileDetails, ProfileType, My_User, Secret_Key
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User , Permission, Group, AbstractUser, AbstractBaseUser
from django.contrib.contenttypes.models import ContentType

class User_Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PermissionList_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class Group_Serializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'

class AbstractUser_Serializer(serializers.ModelSerializer):
    class Meta:
        model = AbstractUser
        fields = '__all__'


class Profile_Details_Serializers(serializers.ModelSerializer):
    class Meta:
        model = ProfileDetails
        fields = "__all__"

class Profile_Type_Serializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileType
        fields = "__all__"


class My_User_Serializer(serializers.ModelSerializer):

    class Meta:
        model = My_User
        fields = ('username', 'email', 'password', 'full_name', 'age', 'address')
        extra_kwargs = {'password': {'write_only': True}}   # make password hash

    def create(self, validated_data):
        user = My_User(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.full_name = validated_data['full_name']
        user.age = validated_data['age']
        user.address = validated_data['address']
        user.save()
        Token.objects.create(user=user)                     # for creating token for the user
        return user

class My_User_Table(serializers.ModelSerializer):
    class Meta:
        model = My_User
        fields = ('id','username', 'email', 'full_name', 'age', 'address')

class My_Sec_Key(serializers.ModelSerializer):
    class Meta:
        model = Secret_Key
        fields = ('id', 's_key', 's_name')