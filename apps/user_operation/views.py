from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import mixins

from .models import UserFav, UserLeavingMessage, UserAddress
from .serializers import UserFavSerializer, UserFavDetailSerializer,LeavingMessageSerializer,AddressSerializer

#用户权限
#为什么要设置用户权限，判断删除操作的用户是否登录用户
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

#单独设置JWT验证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication  #提供token对JWT进行身份验证，拿到数据


# Create your views here.

class UserFavViewset(viewsets.GenericViewSet,mixins.CreateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,mixins.ListModelMixin):
    '''
    list:
        获取用户收藏列表
    retrieve:
        判断某个商品是否已经收藏
    create:
        收藏商品
    '''
    # queryset = UserFav.objects.all()   #下面的get_queryset就是指定返回的数据
    # serializer_class = UserFavSerializer   #下面动态设置了

    # 用户权限
    permission_classes = (IsAuthenticated,IsOwnerOrReadOnly)  #没有权限则弹出框框提示登录，不想弹框就要设置下面，自动判断是否登录
    authentication_classes = (JSONWebTokenAuthentication,SessionAuthentication)  #不设置就会提示登录，设置了需要加入SessionAuthentication后台登录

    lookup_field = 'goods_id'
    #获取当前用户的收藏列表
    def get_queryset(self):
        return UserFav.objects.filter(user=self.request.user)


    #下面这2种功能也可以用信号量（signals）实现，DRF在create和delete的时候都会发送信号量
    #信号量（signals）的使用：1.signals.py文件   2.apps里面添加，如users/apps.py
    #信号量（signals）的使用用不了，继续用下面的

    #重写功能，添加收藏数加一
    def perform_create(self, serializer):
        instance = serializer.save()
        #添加收藏数加一
        goods = instance.goods
        goods.fav_num +=1
        goods.save()

    # 重写功能，添加收藏数减一
    def perform_destroy(self, instance):
        instance.delete()
        #添加收藏数减一
        goods = instance.goods
        goods.fav_num -=1
        goods.save()

    # 动态获取Serializer
    # 动态单独设置序列化表单，因为注册和用户详情返回的数据不一样，用户详情需要单独设置
    def get_serializer_class(self):
        if self.action == "list": #如果是获取详细信息
            return UserFavDetailSerializer
        elif self.action == "create":
            return UserFavSerializer

        return UserFavSerializer


    # def dispatch(self, request, *args, **kwargs):
    #     return super(UserFavViewset,self).dispatch(request,*args, **kwargs)


class LeavingMessageViewset(mixins.ListModelMixin,mixins.DestroyModelMixin,mixins.CreateModelMixin,viewsets.GenericViewSet):
    '''
    list:
        获取用户留言
    create:
        添加留言
    delete:
        删除留言
    '''
    serializer_class = LeavingMessageSerializer

    #用户登录权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 没有权限则弹出框框提示登录，不想弹框就要设置下面，自动判断是否登录
    authentication_classes = (
    JSONWebTokenAuthentication, SessionAuthentication)  # 不设置就会提示登录，设置了需要加入SessionAuthentication后台登录

    # 获取当前用户的留言列表
    def get_queryset(self):
        return UserLeavingMessage.objects.filter(user=self.request.user)

# class AddressViewset(mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin,viewsets.GenericViewSet,mixins.UpdateModelMixin):
class AddressViewset(viewsets.ModelViewSet):  #继承所有的mixins
    '''
    收货地址管理
    list:
        获取收货地址
    craate:
        添加收货地址
    update:
        更新收货地址
    delete:
        删除收货地址
    '''

    serializer_class = AddressSerializer

    #用户登录权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 没有权限则弹出框框提示登录，不想弹框就要设置下面，自动判断是否登录
    authentication_classes = (
    JSONWebTokenAuthentication, SessionAuthentication)  # 不设置就会提示登录，设置了需要加入SessionAuthentication后台登录

    # 获取当前用户的留言列表
    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)