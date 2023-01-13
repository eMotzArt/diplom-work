from django.contrib.auth import login, logout
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from core.models import User
from core.serializers import UserCreateSerializer, ProfileRetrieveUpdateSerializer, UserLoginSerializer


# Create your views here.


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

# CreateAPIViewLoginMethod
class LoginViaCreateAPIView(CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_object(self):
        return User.objects.get(username=self.request.data['username'])

# GenericAPIViewLoginMethod
class LoginViaGenericAPIView(GenericAPIView):
    serializer_class = UserLoginSerializer
    queryset = User.objects.all()

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.get_object()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response(ProfileRetrieveUpdateSerializer(user).data, status=status.HTTP_200_OK)

    def get_object(self):
        return User.objects.get(username=self.request.data['username'])


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProfileRetrieveUpdateSerializer
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'message': 'Logout successfully complete'}, safe=False, status=status.HTTP_204_NO_CONTENT)
