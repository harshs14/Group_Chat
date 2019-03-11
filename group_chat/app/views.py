import json
import random
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import generics, permissions, status, mixins
from django.contrib.auth.models import User
from .serializers import *
from rest_framework.decorators import action
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

        token = random.randint(1000, 10000)
        print(token)
        user = User.objects.create_user(email=email, username=username, password=password)
        otp_obj = Otp.objects.create(user_id=user, otp=token)

        user.is_active = False
        user.save()

        # current_site = get_current_site(request)
        subject = 'GROUP CHAT VERIFICATION'
        # message = render_to_string('app/acc_active_email.html', {
        #
        #     'user': user,
        #     'domain': current_site.domain,
        #     'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode,
        #     'token': account_activation_token.make_token(user),
        # })
        message = "YOUR OTP:- " + str(otp_obj.otp)
        from_mail = EMAIL_HOST_USER
        to_mail = [user.email]
        send_mail(subject, message, from_mail, to_mail, fail_silently=False)
        # messages.success(request, 'VERIFY YOUR EMAIL.')

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


class ActivateOtp(APIView):
    queryset = User.objects.all()
    serializer_class = OtpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, user_id, *args, **kwargs):

        serializer = OtpSerializer(data=request.data)
        if serializer.is_valid():
            otp_obj = Otp.objects.get(user_id=user_id)
            user = User.objects.get(pk=user_id)

            print(otp_obj)
            print(otp_obj.otp)
            print(serializer.data.get('otp'))
            if otp_obj.otp == serializer.data.get('otp'):
                print("hi")
                user.is_active = True
                user.save()
                otp_obj.delete()
                return Response("VERIFIED")
            else:
                return Response("INVALID OTP")
        else:
            return Response("INVALID OTP")


class ForgetPasswordEmail(APIView):
    queryset = User.objects.all()
    serializer_class = ForgetPasswordEmailSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        serializer = ForgetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            user_obj = User.objects.get(email=email)

            # old_otp_obj = Otp.objects.get(user_id=user_obj)
            # if old_otp_obj:
            #     old_otp_obj.delete()

            if user_obj:
                token = random.randint(1000, 10000)
                print(token)
                otp_obj = Otp.objects.create(user_id=user_obj, otp=token)

                subject = 'GROUP CHAT PASSWORD RECOVERY'
                message = "YOUR OTP:- " + str(otp_obj.otp)
                from_mail = EMAIL_HOST_USER
                to_mail = [user_obj.email]
                send_mail(subject, message, from_mail, to_mail, fail_silently=False)

                return Response({'info': 'OTP SENT', 'user_id': user_obj.id})
            else:
                return Response({'info': 'EMAIL NOT FOUND'})
        else:
            return Response({'info': 'ENTER VALID EMAIL'})


class ForgetPasswordOtp(APIView):
    queryset = User.objects.all()
    serializer_class = ForgetPasswordOtpSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, user_id, *args, **kwargs):

        serializer = ForgetPasswordOtpSerializer(data=request.data)
        if serializer.is_valid():
            otp = serializer.data.get('otp')
            otp_obj = Otp.objects.get(user_id=user_id)
            user_obj = User.objects.get(pk=user_id)
            new_password = serializer.data.get('new_password')
            confirm_password = serializer.data.get('confirm_password')

            if otp_obj.otp == otp:
                if new_password == confirm_password:
                    user_obj.password = new_password
                    return Response({'info': 'password changed'})
                else:
                    return Response({'info': 'passwords do not  match'})
            else:
                return Response({'info': 'INVALID OTP'})
        else:
            return Response({'info': 'INAVLID OTP'})


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
                return Response({'user_id': user.id}, status=status.HTTP_200_OK)
            else:
                return Response({'info': 'verify email first'}, status=status.HTTP_200_OK)
        else:
            return Response({'info': 'wrong credentials'}, status=status.HTTP_200_OK)


class UserProfile(generics.GenericAPIView, mixins.UpdateModelMixin, mixins.RetrieveModelMixin):

    queryset = User.objects.all()
    lookup_field = 'id'
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly)
    # parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get(self, request, id, *args, **kwargs):
        return self.retrieve(request, id)

    def put(self, request, id, *args, **kwargs):
        return self.update(request, id)


class CreateGroups(APIView):

    # queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)
    # parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):

        serializer = GroupSerializer(data=request.data)
        user_obj = self.request.user

        if serializer.is_valid():
            serializer.save(admin=user_obj)
            g_id = serializer.data.get('id')
            print(g_id, "hi")
            group = Group.objects.get(id=g_id)
            print(group)
            group.members.add(user_obj)
            return Response({"group_id": g_id}, status=status.HTTP_201_CREATED)


class GroupProfile (viewsets.ModelViewSet):

    queryset = Group.objects.all()
    lookup_url_kwarg = 'id'
    # serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsGroupAdminOrReadOnly)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_serializer_class(self):
        if self.action == ('add_member' or 'delete_member'):
            return MemberSerializer
        elif self.action == 'delete_member':
            return MemberSerializer
        elif self.action == 'member_list':
            return MemberSerializer
        else:
            return GroupSerializer

    @action(detail=True, methods=['PUT'])
    def add_member(self, request, *args, **kwargs):

        serializer = MemberSerializer(data=request.data)
        if serializer.is_valid():
            group = Group.objects.get(id=kwargs['id'])
            print(group)
            data = serializer.data.get('member_data')
            print(data)
            for key, value in data.items():
                value = data[key]
                print(data)
                member_obj = User.objects.get(phone_number=value)
                print(member_obj)
                if member_obj:
                    group.members.add(member_obj)
            return Response("working")
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['PUT'])
    def delete_member(self, request, *args, **kwargs):

        serializer = MemberSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            group = Group.objects.get(id=kwargs['id'])
            print(group)
            data = serializer.data.get('member_data')
            print(data)
            for key, value in data.items():
                value = data[key]
                print(data)
                member_obj = User.objects.get(phone_number=value)
                print(member_obj)
                if member_obj:
                    group.members.remove(member_obj)
            return Response("working")

    @action(detail=True, methods=['PUT'])
    def member_list(self, request, *args, **kwargs):

        serializer = MemberSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            b = {}
            y = []
            group = Group.objects.get(id=kwargs['id'])
            print(group)
            data = serializer.data.get('member_data')
            print(data)
            g_id = Group.objects.filter(id=kwargs['id'])
            for key, value in data.items():
                a = {}
                value = data[key]
                print(data)
                member_obj = User.objects.get(phone_number=value)
                print(member_obj)
                already_member = Group.objects.filter(members=member_obj)
                common_group = set(g_id).intersection(set(already_member))
                if common_group:
                    pass
                else:
                    a.update({key: value})
                    y.append(a)
                    print(y)
            b.update({'member_list': y})
            print(b)
            return Response(b)


class ContactList(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def post(self, request, *args, **kwargs):

        a = {}
        b = {}
        y = []
        data = request.data
        # print(data)
        for key, value in data.items():
            a = {}
            value = data[key]
            # print(value)
            x = User.objects.filter(phone_number=value)
            if x:
                a.update({key: value})
                y.append(a)
                # print(y)
        b.update({'contact': y})
        # print(b)
        return Response(b)


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
            y = set(g).intersection(set(member))
            if y:
                serializer.save(messaged_by=user_obj, group=group)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response({'info': 'not allowed'})

    def get(self, request, g_id, id=None, *args, **kwargs):

        user_obj = request.user
        g = Group.objects.filter(pk=g_id)
        member = Group.objects.filter(members=user_obj)
        y = set(g).intersection(set(member))
        if y:
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


class TestMessage(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin):

    queryset = GroupMessage.objects.all()
    lookup_field = 'id'
    serializer_class = MessageSerializer
    permission_classes = (permissions.IsAuthenticated, IsMessageOwner, IsGroupMember)
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'group_messages.html'

    def post(self, request, g_id, *args, **kwargs):

        test_group = get_object_or_404(Group, pk=g_id)
        group = get_object_or_404(Group, pk=g_id)
        user_obj = self.request.user
        g = Group.objects.filter(pk=g_id)
        member = Group.objects.filter(members=user_obj)
        y = set(g).intersection(set(member))
        if y:
            group_messages = GroupMessage.objects.filter(group=g_id)
            # serializer = MessageSerializer(group_messages)
            serializer = MessageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(messaged_by=user_obj, group=group)
            return render(request, "group_messages.html",
                          {'group_messages': group_messages, "serializer": serializer, "test_group": test_group,
                           })

    def get(self, request, g_id, id=None, *args, **kwargs):

        user_obj = request.user
        test_group = get_object_or_404(Group, pk=g_id)
        g = Group.objects.filter(pk=g_id)
        member = Group.objects.filter(members=user_obj)
        y = set(g).intersection(set(member))
        if y:
            group_messages = GroupMessage.objects.filter(group=g_id)
            # gr = get_object_or_404(Group, pk=g_id)
            # serializer = ProfileSerializer(profile)
            serializer = MessageSerializer(group_messages)
            return Response({'group_messages': group_messages, "test_group": test_group, "serializer": serializer})
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


class ExitGroup(APIView):

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated, IsGroupMember)
    lookup_field = 'g_id'

    def get(self, request, *args, **kwargs):
        group = Group.objects.get(id=kwargs['g_id'])
        user_obj = self.request.user
        group.members.remove(user_obj)
        return Response({"info": "you left group"})


class Logout(APIView):

    def get(self, request, *args, **kwargs):

        logout(request)
        return Response({'info': 'logged out'})
