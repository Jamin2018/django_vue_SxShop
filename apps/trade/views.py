from django.shortcuts import render
from rest_framework import viewsets

#用户权限
#为什么要设置用户权限，判断删除操作的用户是否登录用户
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly

#单独设置JWT验证
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication  #提供token对JWT进行身份验证，拿到数据

from .models import ShoppingCart, OrderGoods ,OrderInfo

from .serializers import ShopCartSerializer, ShopCartDetailSerializer , OrderSerializer, OrderDetailSerializer

#订单功能
from rest_framework import mixins

#随机订单号
import time

# Create your views here.


class ShoppingCarViewset(viewsets.ModelViewSet):
    '''
    购物车功能开发
    list:
        获取购物车详情
    create:
        加入购物车
    delete:
        删除购物车
    '''
    serializer_class =  ShopCartSerializer

    #用户登录权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 没有权限则弹出框框提示登录，不想弹框就要设置下面，自动判断是否登录
    authentication_classes = (
    JSONWebTokenAuthentication, SessionAuthentication)  # 不设置就会提示登录，设置了需要加入SessionAuthentication后台登录
    # queryset = ShoppingCart.objects.all()
    lookup_field = 'goods_id'

    # 获取当前用户的留言列表
    def get_queryset(self):
        return ShoppingCart.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == 'list':
            return ShopCartDetailSerializer
        else:
            return ShopCartSerializer

    #减少库存
    def perform_create(self, serializer):
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums   #这里有bug，每次加入购物车，会根据购物车里面的数量减少库存，应该根据加入购物车的数量减少
        goods.save()
    #增加库存
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()   #要在实例被删除前取数据

    #更新后库存数
    def perform_update(self, serializer):
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums

        saved_record = serializer.save()
        nums = saved_record.nums - existed_nums  #判断修改前后的数量
        goods = saved_record.goods
        goods.goods_num -= nums
        goods.save()

class OrderViewset(viewsets.GenericViewSet,mixins.RetrieveModelMixin,mixins.ListModelMixin,mixins.CreateModelMixin,mixins.DestroyModelMixin):
    '''
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create:
        新增订单
    '''

    #用户登录权限
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)  # 没有权限则弹出框框提示登录，不想弹框就要设置下面，自动判断是否登录
    authentication_classes = (
    JSONWebTokenAuthentication, SessionAuthentication)  # 不设置就会提示登录，设置了需要加入SessionAuthentication后台登录
    serializer_class = OrderSerializer

    def get_queryset(self):
        return OrderInfo.objects.filter(user = self.request.user)


    # 动态获取Serializer
    # 动态单独设置序列化表单，因为注册和用户详情返回的数据不一样，用户详情需要单独设置
    def get_serializer_class(self):
        if self.action == "retrieve": #如果是获取详细信息
            return OrderDetailSerializer
        return OrderSerializer

    #定义POST请求
    def perform_create(self, serializer):
        order = serializer.save() #生成订单
        shop_carts = ShoppingCart.objects.filter(user = self.request.user) # 找到该用户的购物车详情
        for shop_cart in shop_carts:    #逐一加入，生成订单
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_num = shop_cart.nums
            order_goods.order = order
            order_goods.save()
            shop_cart.delete()  #删除购物车详情
        return order
