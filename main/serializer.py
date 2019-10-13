import hashlib

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.response import Response

from .models import User
from .token import decode
from django.conf import settings


class Result(serializers.Serializer):

    #自定义异常（400X为用户端错误， 500X为服务端错误）
    ACTC_EXPIRED = (4001, "无效的激活码")
    ACTC_INVALID = (4002, "激活码已过期")
    USER_NOT_EXISTS = (4003, "用户不存在, 或输入信息有误")
    KEY_ERROR = (4004, "参数有误")
 

    MULITIPLE_OBJECT = (5001, "找到多个用户，请重新注册或联系管理员")

    code = serializers.IntegerField(help_text="状态码")
    msg = serializers.CharField(help_text="帮助信息")
    data = serializers.CharField(allow_blank = True, help_text="数据")

    def create(self, validated_data):
        return Response(self.data)

    @staticmethod
    def success(code=200, msg="success", data=""):
        data = {
            "code": code,
            "msg": msg,
            "data": data
        }

        res = Result(data = data)
        res.is_valid(raise_exception=True)
        return res.save()

    @staticmethod
    def error(err, data = ""):
        code, msg = err
        return Result.success(code, msg, data)

class UserOPS(object):
    class Register(serializers.Serializer):
        username = serializers.CharField(max_length = 20, min_length = 4, trim_whitespace = True)
        email = serializers.EmailField(help_text="目前邮箱只支持@stu.edu.cn")
        password = serializers.CharField(min_length = 8, max_length = 20, trim_whitespace = True)

        def validate(self, data):

            #校验邮箱后缀
            if "@stu.edu.cn" not in data["email"]:
                raise serializers.ValidationError("邮箱格式有误")

            #校验用户名合法性 TODO
            #校验密码合法性 TODO
            return data

        def create(self, validated_data):
            validated_data["password"] = hashlib.sha512(str(settings.SECRET_KEY + validated_data["password"]).encode("UTF-8")).hexdigest()
            return User.objects.create(**validated_data)


    class Login(serializers.Serializer):
        credence = serializers.CharField(max_length = 20, min_length = 4, trim_whitespace = True, help_text="凭证（用户名和密码）")
        password = serializers.CharField(min_length = 8, max_length = 20, trim_whitespace = True)

        def create(self, validated_data):
            password = hashlib.sha512(str(settings.SECRET_KEY + validated_data["password"]).encode("UTF-8")).hexdigest()
            credence = validated_data["credence"]

            try:
                user = User.objects.get(username=credence, password=password)
            except ObjectDoesNotExist:
                user = User.objects.get(email=credence, password=password)
            
            return user


    class Activate(serializers.Serializer):
        token = serializers.CharField(trim_whitespace = True)

        def validate(self, data):
            data["token"] = decode(data["token"])
            return data

        def create(self, validated_data):
            decoded_token = validated_data["token"]
            return User.objects.get(pk=decoded_token.get('pk'))

        def update(self, instance, validated_data):
            instance.is_active = 1
            instance.save()
            return instance
