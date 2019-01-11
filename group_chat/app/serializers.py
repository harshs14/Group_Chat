from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Message, Group
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


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
        model = User
        fields = ('name', 'avatar', 'phone_number')
        # read_only_fields = ('user',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('name', 'avatar', 'admin', 'members')
        read_only_fields = ('admin', 'members')


class AddMemberSerializer(serializers.ModelSerializer):
    members = UserProfileSerializer(many=True)

    class Meta:
        model = Group
        fields = ('name', 'members',)
