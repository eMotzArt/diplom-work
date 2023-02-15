from collections import OrderedDict

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers

from core.models import User
from goals.models import Board, BoardParticipant


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate_password(self, password: str) -> str:
        validate_password(password=password, user=User)
        return password

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        if attrs['password'] != attrs.pop('password_repeat'):
            raise serializers.ValidationError('Passwords do not match',)
        return super().validate(attrs)

    def create(self, validated_data: dict) -> User:
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()

        # create default user board
        first_user_board = Board.objects.create(
            title="Мои цели",
            created=timezone.now(),
            updated=timezone.now()
        )

        BoardParticipant.objects.create(
            user=user,
            board=first_user_board,
            role=BoardParticipant.Role.owner,
            created=timezone.now(),
            updated=timezone.now()
        )

        return user


class ProfileRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class PasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    new_password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['old_password', 'new_password']

    def validate_new_password(self, password: str) -> str:
        validate_password(password=password, user=self.instance)
        return password

    def validate_old_password(self, password: str) -> str:
        # Возможность залогинившихся через VK OAuth2 задать пароль
        if (self.instance.password[:13] != 'pbkdf2_sha256' and self.instance.password[:1] == '!') \
                or self.instance.check_password(password):
            return password
        raise serializers.ValidationError('Password is incorrect')


    def update(self, instance: User, validated_data: dict) -> User:
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs: OrderedDict) -> OrderedDict:
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Username or password is incorrect')
        return attrs
