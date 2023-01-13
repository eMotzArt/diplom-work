from django.contrib.auth import login
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from core.models import User
from core.serializers import UserCreateSerializer, UserLoginSerializer


# Create your views here.


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()


# GenericAPIViewLoginMethod
class LoginViaGenericAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response({'status': 'ok'}, status=status.HTTP_200_OK)

    def get_object(self):
        return User.objects.get(username=self.request.data['username'])

