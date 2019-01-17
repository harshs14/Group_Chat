import json
from rest_framework import generics, permissions, status, mixins
from django.contrib.auth.models import User
from .serializers import *
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
from . models import *
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .permissions import *         
from rest_framework import filters

# -----------------------User Registration/Signup------------------------------------------------------------------
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

#
# class CreateUserProfile(generics.ListCreateAPIView):
#
#     queryset = User.objects.all()
#     serializer_class = UserProfileSerializer
#     permission_classes = (permissions.IsAuthenticated,)
#
#     def post(self, request, *args, **kwargs):
#
#         serializer = UserProfileSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save(user=self.request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfile(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id)

    def put(self, request, id, *args, **kwargs):
        return self.update(request, id)


class CreateGroups(generics.GenericAPIView, mixins.ListModelMixin):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):

        serializer = GroupSerializer(data=request.data)
        user_obj = self.request.user

        if serializer.is_valid():
            serializer.save(admin=self.request.user)
            g_id = serializer.data.get('id')
            group = Group.objects.get(pk=g_id)
            group.members.add(user_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_obj = self.request.user

        return self.list(request)


class GroupProfile (generics.GenericAPIView,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin):

    queryset = Group.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsGroupAdminOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id)

    def put(self, request, id, *args, **kwargs):
        return self.update(request, id)

    def delete(self, request, id, *args, **kwargs):
        return self.destroy(request, id)


# class ContactList(APIView):
#
#     def post(self, request, *args, **kwargs):
#
#         data = json.loads(request.body)
#         contact_list = data['number']
#         for i in contact_list:
#             j = User.objects.filter(phone_number=i)
#         return Response({'user_list': j})


# class AddMember(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.DestroyModelMixin,mixins.RetrieveModelMixin):
#
#     queryset = Group.objects.all()
#     serializer_class = AddMemberSerializer
#     permission_classes = (permissions.IsAuthenticated, )
#     lookup_url_kwarg = 'id'
#
#     def put(self, request, id, *args, **kwargs):
#
#         member = Group.members.add(User.objects.get(phone_number=request.data))
#         serializer = AddMemberSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save(members=member)
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request, id, *args, **kwargs):
#         return self.retrieve(request, id)


class Message(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    queryset = GroupMessage.objects.all()
    lookup_field = 'id'
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsMessageOwner, IsGroupMember)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, g_id, *args, **kwargs):

        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            user_obj = request.user
            group = Group.objects.get(pk=g_id)
            g = Group.objects.filter(pk=g_id)
            member = Group.objects.filter(members=user_obj)
            for x in member:
                if g == x:
                    a = 1
            if a == 1:
                serializer.save(messaged_by=user_obj, group=group)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'info': 'not allowed'})

    def get(self, request, g_id, id=None, *args, **kwargs):

        user_obj = request.user
        group = Group.objects.get(pk=g_id)
        member = Group.objects.filter(members=user_obj)
        # print(group,'hi')
        # print(member,'hi')
        if member == group:
            group_messages = GroupMessage.objects.filter(group=g_id)
            serializer = MessageSerializer(group_messages, many=True)
            return Response(serializer.data)
        else:
            return Response({'info': 'not allowed'})

    def delete(self, request, g_id, id=None, *args, **kwargs):

        if id:
            return self.destroy(request, g_id, id)
        else:
            pass


class GroupList(generics.GenericAPIView):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    filter_backends = (filters.SearchFilter,)
    search_fields = 'name'

    def get(self, request, *args, **kwargs):

        user_obj = request.user
        g = Group.objects.filter(members=user_obj)
        serializer = GroupSerializer(g, many=True)
        return Response(serializer.data)


class Logout(APIView):

    def get(self, request, *args, **kwargs):

        logout(request)
        return Response({'info': 'logged out'})