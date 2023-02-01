from rest_framework import serializers

from bot.models import TgUser


class TgUserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = '__all__'
        # read_only_fields = ('id', 'user', 'created', 'updated', 'is_deleted', 'board')
