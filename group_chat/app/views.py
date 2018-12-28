from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from app.serializers import UserRegisterSerializer, UserLoginSerializer, UserProfileSerializer
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


# -----------------------User Registration/Signup-------------------------------------------------------------------
class Register(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        user = User.objects.create_user(first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),
                                        email=request.POST.get('email'),
                                        username=request.POST.get('username'),
                                        password=request.POST.get('password'))

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

        return Response({'info': 'user created'}, status=status.HTTP_201_CREATED)


class Activate(View):

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

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return Response({'info': 'logged in'}, status=status.HTTP_200_OK)
            else:
                return Response({'info': 'verify email first'}, status=status.HTTP_200_OK)

        else:
            return Response({'info': 'wrong credentials'}, status=status.HTTP_200_OK)

#     def get(self, request, *args, **kwagrs):
#         if request.user.is_authenticated:
#             return redirect('home')
#
#
# class Home(generics.ListCreateAPIView):
#
#     def get(self, request, *args, **kwargs):
#
#         return Response({'info': 'hi, you are logged in'}, status=status.HTTP_200_OK)


class UserProfile(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        # user_obj = request.user.username
        # gender = request.POST['gender']
        # dob = request.POST['date_of_birth']
        # avatar = request.FILES['avatar']
        # phone_no = request.POST['phone_no']

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            member = serializer.save(commit=False)
            member.user = request.user.username
            member.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

