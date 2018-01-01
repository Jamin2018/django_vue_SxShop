# -*- coding:utf-8 -*-

from rest_framework import serializers
from .models import UserFav
from goods.serializers import GoodsSerializer

#自定义报错信息
from rest_framework.validators import UniqueTogetherValidator

from .models import UserLeavingMessage,UserAddress

#用户显示收藏
class UserFavDetailSerializer(serializers.ModelSerializer):
    #因为外键不是自己，所以可以不用反向关联键
    #设置一个反向关联试试,报错了，上面不成立
    goods = GoodsSerializer()
    # text = GoodsSerializer()   # 报错
    class Meta:
        model = UserFav
        fields = ('goods', 'id',)
        # fields = "__all__"

class UserFavSerializer(serializers.ModelSerializer):
    #只获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    class Meta:
        model = UserFav

        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields = ('user','goods'),
                message='已收藏',
            )
        ]


        fields =  ('user','goods','id',)

#用户留言
class LeavingMessageSerializer(serializers.ModelSerializer):

    #只获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    #只显示，不提交这个数据，并且格式化前端的显示问题
    #format
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserLeavingMessage

        fields = ('user', 'message_type', 'subject','message','file','id','add_time')


class AddressSerializer(serializers.ModelSerializer):
    #只获取当前用户
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault(),
    )
    #只显示，不提交这个数据，并且格式化前端的显示问题
    #format
    add_time = serializers.DateTimeField(read_only=True,format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = UserAddress

        fields = ('id','user', 'province', 'city','district','address','signer_name','add_time','signer_mobile')