import jwt
from django.conf import settings
secret = "*&B*&gbir7ftywd%^"

def encode_jwt(data):
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_jwt(data):
    decoded_jwt = jwt.decode(data, settings.SECRET_KEY, algorithms=["HS256"])
    return decoded_jwt
