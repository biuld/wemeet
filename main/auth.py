from rest_framework.authentication import BaseAuthentication
from .token import decode
from rest_framework.exceptions import AuthenticationFailed
from jwt import ExpiredSignatureError, DecodeError
from .models import User



class Auth(BaseAuthentication):

    def authenticate(self, request):
        
        token = request.META.get("HTTP_AUTHORIZATION", "")

        if not token:
            return None

        try:
            data = decode(token)
        except ExpiredSignatureError:
            raise AuthenticationFailed("token expired") 
        except DecodeError:
            raise AuthenticationFailed("decode error")  

        pk = data.get("pk", "")

        if not pk :
            raise AuthenticationFailed("couldn't find the declared field id")

        try:
            user = User.objects.get(pk=pk)
        except Exception as e:
            raise AuthenticationFailed("error while looking up database, {}".format(str(e)))

        return user, None
