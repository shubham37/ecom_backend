from django.contrib.auth.models import User
from rest_framework import exceptions
from api.models import User
from rest_framework import authentication
from rest_framework import exceptions


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('HTTP_X_TOKEN')
        if not token:
            return None

        try:
            user = User.objects.get(token=token)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)
