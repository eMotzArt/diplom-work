from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import check_password
from rest_framework import serializers

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'password_repeat']

    def validate_password(self, password):
        validate_password(password=password, user=User)
        return password

    def validate(self, attrs):
        if attrs['password'] != attrs.pop('password_repeat'):
            raise serializers.ValidationError('Passwords do not match',)
        return super().validate(attrs)

    def create(self, validated_data):
        # validate_password(validated_data['password'], User)
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
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

    def validate_new_password(self, password):
        validate_password(password=password, user=self.instance)
        return password

    def validate_old_password(self, password):
        # Возможность залогинившихся через VK OAuth2 задать пароль
        if (self.instance.password[:13] != 'pbkdf2_sha256' and self.instance.password[:1] == '!') \
                or self.instance.check_password(password):
            return password
        raise serializers.ValidationError('Password is incorrect')


    def update(self, instance, validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, style={'input_type': 'password'})

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Username or password is incorrect')
        return attrs
