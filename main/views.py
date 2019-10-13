
import hashlib

from django.conf import settings
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render
from .models import User
from .email import send_activate_mail
from .token import encode, JWT_TTL_ALT
from .serializer import UserOPS, Result


@swagger_auto_schema(
    operation_description="登陆",
    request_body=UserOPS.Login,
    method = 'post',
    tags=["登陆"],
    responses= {200: Result}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):

    srl = UserOPS.Login(data=request.data)
    srl.is_valid(raise_exception=True)
    user = srl.save()

    return Result.success(data=encode(user.pk))

@swagger_auto_schema(
    operation_description="激活",
    query_serializer=UserOPS.Activate,
    method = 'get',
    tags=["激活用户"],
    responses= {200: Result}
)
@api_view(['GET'])
@permission_classes([AllowAny])
def activate(request):

    srl = UserOPS.Activate(data = request.query_params)
    srl.is_valid(raise_exception=True)
    user = srl.save()
    
    if user.is_active != 1:
        srl.save(instance = user, validated_data = {"is_active": 1})
    
    return render(request, 'activation_success.html')


@swagger_auto_schema(
    operation_description="注册",
    request_body=UserOPS.Register,
    method = 'post',
    tags=["注册"],
    responses= {200: Result}
)
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):

    srl = UserOPS.Register(data=request.data)

    srl.is_valid(raise_exception=True)
    user = srl.save()

    token = encode(user.pk, JWT_TTL_ALT)
    send_activate_mail(request, user.email, '激活账号', 'email', token=token, username=user.pk)

    return Result.success(msg="注册成功")
