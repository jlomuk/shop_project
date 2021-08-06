from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User


class EmailAuthBackend(BaseBackend):
    """Добавляет возможность аутентификации по почте"""

    def authenticate(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=kwargs['username'])
            if user.check_password(kwargs['password']):
                return user
        except:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
