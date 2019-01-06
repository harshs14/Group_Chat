from rest_framework import generics, permissions, status, mixins
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer, GroupSerializer, \
    AddMemberSerializer
from rest_framework.response import Response
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.core.mail import send_mail
from group_chat.settings import EMAIL_HOST_USER
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.http import HttpResponse
from rest_framework.views import APIView
from . models import Member, Message, Group


# -----------------------User Registration/Signup-------------------------------------------------------------------
class Register(APIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')

        if email is None:
            return Response({'info': 'enter email!!!'})

        if password is None:
            return Response({'info': 'enter password!!!'})

        if password != confirm_password :
            return Response({'info': 'password does not match'})

        if User.objects.filter(username=username):
            return Response({'info': 'username exits!!!'})

        if User.objects.filter(email=email):
            return Response({'info': 'email exits!!!'})

        user = User.objects.create_user(email=email, username=username, password=password)

        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        subject = 'GROUP CHAT VERIFICATION'
        message = render_to_string('app/acc_active_email.html', {

            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
            'token': account_activation_token.make_token(user),
        })
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        messages.success(request, 'VERIFY YOUR EMAIL.')

        return Response({'info': 'user created', 'user_id': user.id}, status=status.HTTP_201_CREATED)


class Activate(APIView):

    def get(self, request, token, uidb64):

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, 'EMAIL VERIFIED')
            return redirect("register")

        else:
            messages.error(request, "Activation Email Link is Invalid.Please try again!!")
            return redirect('register')


class Login(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        username = request.data['username']
        password = request.data['password']

        if username is None:
            return Response({'info': 'enter username!!!'})

        if password is None:
            return Response({'info': 'enter password!!!'})

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'info': 'logged in', 'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'info': 'verify email first'}, status=status.HTTP_200_OK)
        else:
            return Response({'info': 'wrong credentials'}, status=status.HTTP_200_OK)


class CreateUserProfile(generics.ListCreateAPIView):

    queryset = Member.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        serializer = UserProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.GenericAPIView,
                  mixins.UpdateModelMixin):

    queryset = Member.objects.all()
    lookup_field = 'user_id'
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, user_id, *args, **kwargs):
        return self.update(request, user_id)


class CreateGroup(generics.ListCreateAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        serializer = GroupSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(admin=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupProfile (generics.GenericAPIView,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin):

    queryset = Group.objects.all()
    lookup_field = 'id'
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, id, *args, **kwargs):
        return self.update(request, id)

    def delete(self, request, id, *args, **kwargs):
        return self.destroy(request, id)


# class AddMember(generics.ListCreateAPIView):
#
#     queryset = Member.objects.all()
#     serializer_class = AddMemberSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#
#     def post(self, request, *args, **kwargs):
#
#         group = Group.objects.get(id=kwargs['pk'])
#         member = Group.members.objects.get(phone_number=request.data)
#
#         serializer = AddMemberSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save(name=group, members=member)
#             return Response({'pk': group}, serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



