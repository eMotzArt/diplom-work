from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from core.models import User


class UserCreateSerializer(serializers.ModelSerializer):
    password_repeat = serializers.CharField(required=True, write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

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

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        user = authenticate(**attrs)
        if not user:
            raise serializers.ValidationError('Username or password is incorrect')
        return attrs
