import secrets
import bcrypt 
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from gym.models import TokenModel
from gym.authentication import expired_token_handler, expires_in
from gym.serializers import LoginSerializer

class LoginController():
    """
    Login contoller
    """
    def _token_generator(self, user):
        key = bcrypt.hashpw(secrets.token_hex(10).encode('utf-8'), bcrypt.gensalt())
        key = key.decode('utf-8')
        token, _ = TokenModel.objects.update_or_create(user=user, defaults={'key':key})
        return token

    def login(self, request):
        """Handles Login"""
        login_serializer = LoginSerializer(data=request.data)
        if not login_serializer.is_valid():
            return Response({'details':login_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=login_serializer.data['username'],
            password=login_serializer.data['password']
        )

        if not user:
            return Response(
                {'details':'Invalid Credentials', 'code':400},
                status=status.HTTP_200_OK
            )

        try:
            token = TokenModel.objects.get(user=user)
        except TokenModel.DoesNotExist:
            token = self._token_generator(user)

        is_expired, token = expired_token_handler(token)
        
        if is_expired:
            token = self._token_generator(user)
        
        
        return Response({
            
            'expires_in': expires_in(token),
            'token': token.key
        }, status=status.HTTP_200_OK)
