# -*- coding:utf-8 -*-

from rest_framework import serializers

from goods.models import Goods
from .models import ShoppingCart, OrderInfo, OrderGoods
from goods.serializers import GoodsSerializer

import time

#Serializer比ModelSerializer更灵活
#自己写最底层
#因为需要数据验证通过，ModelSerializer写不了
class ShopCartSerializer(serializers.Serializer):
    #只获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )

    nums = serializers.IntegerField(label='数量',required=True,min_value=1,error_messages={
        'min_value':'商品数量不能小于1',
        'required':'请选择购买数量',
    })
    #goods是一个外键
    # goods = serializers.PrimaryKeyRelatedField(label='商品',queryset=Goods.objects.all(),required=True,)
    goods = serializers.PrimaryKeyRelatedField(required=True, queryset=Goods.objects.all())

    def create(self, validated_data):
        user = self.context['request'].user  #获取上下文里面的request,Serializer这里的self没有request,Views里面有
        nums = validated_data['nums']
        goods = validated_data['goods']
        existed = ShoppingCart.objects.filter(goods=goods,user=user)

        # 判断购物车是否存在该商品
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    def update(self, instance, validated_data):
        #修改商品数量
        instance.nums = validated_data['nums']
        instance.save()
        return instance


class ShopCartDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False,)
    class Meta:
        model = ShoppingCart
        fields = '__all__'


class OrderGoodsSerialzer(serializers.ModelSerializer):
    goods = GoodsSerializer(many=False)

    class Meta:
        model = OrderGoods
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):

    goods = OrderGoodsSerialzer(many=True)
    class Meta:
        model = OrderInfo
        fields = '__all__'




class OrderSerializer(serializers.ModelSerializer):
    #只获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    #只读不写，不能给用户修改
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)
    add_time = serializers.DateTimeField(read_only=True, format='%Y-%m-%d %H:%M:%S')

    #保存之前生成订单号
    def generate_order_sn(self):
        #当前时间+userid+随机数
        from random import Random
        random_ins = Random()
        order_sn = '{time_str}{userid}{ranstr}'.format(time_str=time.strftime('%Y%m%d%H%M%S'),userid=self.context['request'].user.id,
                                                       ranstr=random_ins.randint(10,99))
        return order_sn

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs
    class Meta:
        model = OrderInfo
        fields = '__all__'