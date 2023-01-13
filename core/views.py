from rest_framework.generics import CreateAPIView
from core.models import User
from core.serializers import UserCreateSerializer


# Create your views here.


class CreateUserView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()

