from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from app.serializers import UserSerializer
from rest_framework.response import Response


# -----------------------User Registration/Signup-------------------------------------------------------------------
class Register(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):

        user = User.objects.create_user(first_name=request.POST.get('first_name'),
                                        last_name=request.POST.get('last_name'),
                                        email=request.POST.get('email'),
                                        username=request.POST.get('username'),
                                        password1=request.POST.get('password'))

        user.save(commit=False)
        user.is_active = False
        user.save()

        return Response({'info': 'user created'}, status=status.HTTP_201_CREATED)


