from rest_framework import generics
from django.contrib.auth.models import User
from app.serializers import UserSerializer


# -----------------------User Registeration/Signup----------------------------------------------------------------------
class Register(generics.ListCreateApiView):

    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        user = User.objects.create_user(name=request.POST.get('name'),
                                        email=request.POST.get('email'),
                                        username=request.POST.get('username'),
                                        password=request.POST.get('password'))

        user.save(commit=False)
        user.is_active = False
        user.save()


