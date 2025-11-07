# Authenticate with email or username for Customer model

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

Customer = get_user_model()

class EmailOrUsernameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        
        identifier = username or kwargs.get('email') or kwargs.get('username')
        if not identifier or not password:
            return None
        try:
            if '@' in identifier:
                user = Customer.objects.get(email__iexact=identifier)
            else:
                user = Customer.objects.get(username__iexact=identifier)
        except Customer.DoesNotExist:
            return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None