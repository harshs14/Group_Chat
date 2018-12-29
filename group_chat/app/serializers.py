from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Member, Message, Group
from rest_framework.validators import UniqueValidator


class UserRegisterSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # username = serializers.CharField(
    #     required=True,
    #     validators=[UniqueValidator(queryset=User.objects.all())]
    # )
    # password = serializers.CharField(
    #     required=True,
    #     min_length=8)
    #
    # def create(self, validated_data):
    #     user = User.objects.create_user(validated_data['username'], validated_data['email'],
    #                                     validated_data['password'])
    #     return user
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username', 'password',)


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
        fields = ('user', 'avatar', 'date_of_birth', 'gender',)
        read_only_fields = ('user',)




