from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member, Message, Group
from rest_framework.validators import UniqueValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    confirm_password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'confirm_password',)


class UserLoginSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('username', 'password',)


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Member
        fields = ('user', 'name', 'avatar', 'phone_number')
        read_only_fields = ('user',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', 'avatar', 'admin')
        read_only_fields = ('admin',)

