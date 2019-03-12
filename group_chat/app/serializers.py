from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, style={'input_type': 'password'})
    confirm_password = serializers.CharField(required=True, style={'input_type': 'password'})

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
    members = UserProfileSerializer(many=True, read_only=True)
    # admin = UserProfileSerializer()

    class Meta:
        model = Group
        fields = ('id', 'name', 'avatar', 'admin', 'members',)
        read_only_fields = ('admin', 'members', 'id')


class MemberSerializer(serializers.Serializer):
    member_data = serializers.JSONField(allow_null=True)

    class Meta:
        fields = 'member_data'

        # model = Group
        # fields = ('id', 'name', 'avatar', 'admin', 'members')
        # read_only_fields = ('admin',  'id', )


class MessageSerializer(serializers.ModelSerializer):
    # messaged_by = UserProfileSerializer()

    class Meta:
        model = GroupMessage
        fields = ('id', 'message', 'messaged_by', 'file_message', 'time', 'group')
        read_only_fields = ('id', 'time', 'messaged_by', 'group')


class OtpSerializer(serializers.ModelSerializer):

    class Meta:
        model = Otp
        fields = ('user_id', 'otp', 'id')
        read_only_fields = ('user_id', 'id')


class ForgetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        field = 'email'


class ForgetPasswordOtpSerializer(serializers.ModelSerializer):
    new_password = serializers.CharField(required=True, style={'input_type': 'password'})

    confirm_password = serializers.CharField(required=True, style={'input_type': 'password'})

    class Meta:
        model = Otp
        fields = ('user_id', 'otp', 'id', 'new_password', 'confirm_password')
        read_only_fields = ('user_id', 'id')
