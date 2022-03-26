from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from gym.models import TokenModel

def expires_in(token):
    """time left to live for token"""
    elapsed_time = timezone.now() - token.created
    remaining_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - elapsed_time
    return remaining_time

def has_token_expired(token):
    """confirm if token expired"""
    return expires_in(token) < timedelta(seconds=0)

def expired_token_handler(token):
    """Delete expired token"""
    is_expired = has_token_expired(token)
    if is_expired:
        token.delete()
    return is_expired, token


class CustomAuthentication(TokenAuthentication):
    """Custom authentication class"""
    def authenticate_credentials(self, key):
        try:
            self.token = TokenModel.objects.get(key=key)
        except TokenModel.DoesNotExist:
            raise AuthenticationFailed({'details':'Token you are using is invalid', 'code':600})
        
        self.is_expired, self.token = expired_token_handler(self.token)
        
        if self.is_expired:
            raise AuthenticationFailed({'details':'Token you are using has expired', 'code':600})

        if not self.token.user.is_active:
            raise AuthenticationFailed({
                'details':'The user you are using has been deactivated. Contact support',
                'code':603
            })

        return (self.token.user, self.token)
        