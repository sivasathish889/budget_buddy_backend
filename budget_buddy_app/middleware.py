from django.utils.deprecation import MiddlewareMixin
from .utils.jwt import decode_jwt
import jwt
from .models import Users
from .serializer import UserSerializer
class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization') 
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[2]
            try:
                payload = decode_jwt(token)
                user_id = payload.get('id')
                if user_id:
                    # Attach the user to the request
                    user = Users.objects.get(id=user_id)
                    request.current_user = UserSerializer(user).data
                else:
                    request.current_user = None
            except jwt.ExpiredSignatureError:
                request.current_user = None  # Token expired
            except jwt.InvalidTokenError:
                request.current_user = None  # Invalid token
        else:
            request.current_user = None