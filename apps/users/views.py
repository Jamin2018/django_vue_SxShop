from django.shortcuts import render

# Create your views here.
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth import get_user_model  #获得项目默认的User表
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins

# 报错了，卡在第7章的第9小节
#短信验证码
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets
#验证手机是否合法 , 用户表单（）否通过
from .serializers import SmsSerializer ,UserRegSerializer, UserDetailSerializer
from utils.yunpian import YunPian

from SxShop.settings import APIKEY
#生成验证码
# import random
from random import choice

#注册后自动登录
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler

from .models import VerifyCode

#权限设置
from rest_framework import permissions

#单独设置JWT验证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication  #提供token对JWT进行身份验证，拿到数据

User = get_user_model()

class CustomBackend(ModelBackend):
    '''
    自定义用户验证
    '''
    def authenticate(self,username = None, password = None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile = username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewset(CreateModelMixin, viewsets.GenericViewSet):
    """
    发送短信验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        :return:
        """
        seeds = "1234567890"
        random_str = []
        for i in range(4):
            random_str.append(choice(seeds))

        return "".join(random_str)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]

        yun_pian = YunPian(APIKEY)

        code = self.generate_code()

        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status["code"] != 0:
            '''
            sms_status["code"] = 0表示发送成功
            '''
            return Response({
                "mobile":sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            '''
            成功后保存验证码到数据库
            '''
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile":mobile
            }, status=status.HTTP_201_CREATED)


class UserViewset(mixins.UpdateModelMixin,CreateModelMixin,viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin):
    '''
    用户
    '''
    serializer_class = UserRegSerializer  #单独验证表单有没有出错，并返回数据
    queryset = User.objects.all()

    authentication_classes = (
    JSONWebTokenAuthentication, SessionAuthentication)  # 不设置就会提示登录，设置了需要加入SessionAuthentication后台登录
    #动态的设置权限
    # permission_classes = (permissions.IsAuthenticated)
    def get_permissions(self):
        if self.action == "retrieve":  #如果是获取详细信息
            return [permissions.IsAuthenticated()]
        elif self.action == "create":  #如果是post方法
            return []
        return []  #其他情况返回空

    # 动态获取Serializer
    # 动态单独设置序列化表单，因为注册和用户详情返回的数据不一样，用户详情需要单独设置
    def get_serializer_class(self):
        if self.action == "retrieve": #如果是获取详细信息
            return UserDetailSerializer
        elif self.action == "create":
            return UserRegSerializer

        return UserDetailSerializer

    #重新写保存，因为需要返回token，实现页面注册后自动登录
    # create == post方法
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        #收到设置jwt的token值，实现注册后自动登录
        re_dict = serializer.data

        # 不知道为什么要注释才能自动登录。。。本来下面的功能是设置自动注册后登陆
        # 因为用了信号量（signals.py）
        # payload = jwt_payload_handler(user)
        # re_dict["token"] = jwt_encode_handler(payload)
        # re_dict["name"] = user.name if user.name else user.username
        # print(re_dict["token"])
        # print(re_dict["name"])


        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    #重写get方法
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        serializer.save()
