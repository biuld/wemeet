from django.db import models
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .token import encode,decode

# Create your models here.


class User(models.Model):
    SEX_CHOICES = [(1, "男"), (2, "女")]
    ACTIVE_STAT_CHOICES = [(0, "未激活"), (1, "已激活")]

    is_authenticated = True
    is_anonymous = False

    username = models.CharField(unique=True, max_length=128)
    password = models.CharField(max_length=128)  #sha512加密
    email = models.CharField(max_length=128, unique=True)

    is_active = models.PositiveSmallIntegerField(choices=ACTIVE_STAT_CHOICES,
                                                 default=0)

    sex = models.PositiveSmallIntegerField(choices=SEX_CHOICES,
                                           blank=True,
                                           null=True)
    region = models.CharField(max_length=256, blank=True, null=True)
    info = models.CharField(max_length=256, blank=True, null=True)
    avatar = models.CharField(max_length=512, blank=True, null=True)
    bg_pic = models.CharField(max_length=512, blank=True, null=True)


class Activity(models.Model):

    CATEGORY_CHOICES = [(1, "拼车"), (2, "短途出游"), (3, "长途旅行"), (4, "组队练习"),
                        (5, "其他出行")]

    owner = models.ForeignKey(User,
                              on_delete=models.PROTECT,
                              related_name="owner")
    participants = models.ManyToManyField(User, related_name="participants")
    gmt_create = models.DateTimeField(auto_now_add=True)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES)
    location = models.CharField(max_length=128)
    member_count = models.PositiveSmallIntegerField()
    mobile = models.CharField(max_length=128)
    info = models.CharField(max_length=512)
    pictures = models.TextField()