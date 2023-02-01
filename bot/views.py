from django.core.exceptions import MultipleObjectsReturned
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serializers import TgUserVerificationSerializer
from bot.tg.client import TgClient


# Create your views here.

class BotVerification(UpdateAPIView):
    queryset = TgUser.objects.all()
    serializer_class = TgUserVerificationSerializer
    permission_classes = [IsAuthenticated, ]

    def patch(self, request, *args, **kwargs):
        try:
            instance = TgUser.objects.get(verification_code=request.data['verification_code'])
        except KeyError:
            raise PermissionDenied('Verification code not found')
        except TgUser.DoesNotExist:
            raise PermissionDenied('Verification code not correct')
        except MultipleObjectsReturned:
            raise PermissionDenied('Verification code error. Please generate a new verification code and try again.')

        instance.app_user = request.user
        instance.save()

        serializer = self.get_serializer(instance)
        TgClient().send_message(instance.tg_chat_id, 'Verification completed.\n Available commands:\n/goals \n/create')
        return Response(serializer.data)

