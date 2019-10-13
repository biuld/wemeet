import jwt
from django.conf import settings
import time

JWT_TTL = 60 * 60 * 1000 #有效时间一小时
JWT_TTL_ALT = 5 * 60 * 1000 #5分钟


def encode(pk, exp = JWT_TTL):

    load = {
        'pk': pk,
        'exp': exp + int(time.time())
    }

    return jwt.encode(payload=load, key=settings.SECRET_KEY, algorithm='HS256').decode('utf-8')


def decode(encoded):
    return jwt.decode(encoded, key=settings.SECRET_KEY, algorithms='HS256')