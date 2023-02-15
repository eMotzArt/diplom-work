from rest_framework import serializers

from bot.models import TgUser


class TgUserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'
