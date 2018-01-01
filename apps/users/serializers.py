# # -*- coding:utf-8 -*-
## 报错了，卡在第7章的第9小节
#手机验证
import re
from datetime import datetime , timedelta
from .models import VerifyCode

from rest_framework import serializers

from django.contrib.auth import get_user_model  #获得项目默认的User表

from SxShop.settings import REGEX_MOBILE
# 自定义表单字段验证
from rest_framework.validators import UniqueValidator

User = get_user_model()


class SmsSerializer(serializers.Serializer):
    mobile = serializers.CharField(max_length=11)

    def validate_mobile(self, mobile):
        """
        验证手机号码
        :param data:
        :return:
        """

        # 手机是否注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError("用户已经存在")

        # 验证手机号码是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError("手机号码非法")

        # 验证码发送频率
        one_mintes_ago = datetime.now() - timedelta(hours=0, minutes=1, seconds=0)
        if VerifyCode.objects.filter(add_time__gt=one_mintes_ago, mobile=mobile).count():
            raise serializers.ValidationError("距离上一次发送未超过60s")

        return mobile

class UserRegSerializer(serializers.ModelSerializer):
    #user表中没有code，自己添加
    #required=True  必填字段
    #因为每次创建数据后，前端都会收到返回的数据，所以会把code返回，但是后面删了，序列化不了，所以设置不返回
    #设置write_only=True,因为 del attrs['code']，前端序列化的时候没有code所以报错
    #单独设置write_only=True，使前端不序列化code

    code = serializers.CharField(required=True,max_length=4,min_length=4,help_text='验证码',label='验证码',
                                 write_only=True,
                                 error_messages = {
                                     'blank':'请输入验证码',  #这个才是传入的值未空，返回的提示信息
                                     'required':'请输入验证码',
                                     'max_length':'验证码格式错误',
                                     'min_length':'验证码格式错误',
                                 })
    #自定义用户名是否存在的验证方法
    username = serializers.CharField(required=True,allow_blank=False,label='用户名',
                                     validators=[UniqueValidator(queryset=User.objects.all(),message='用户已经存在')])
    #设置密码不返回到前端：write_only=True,
    password = serializers.CharField(
        style={'input_type':'password'},
        label='密码',
        write_only=True,
    )
    # 单独设置在signals.py里面了
    # def create(self, validated_data):
    #     user = super(UserRegSerializer, self).create(validated_data=validated_data)
    #     user.set_password(validated_data["password"])
    #     user.save()
    #     return user


    def validate_code(self, code):
        # 前端传来的数据放在这个里面，所以可以直接取到当前的电话  self.initial_data
        verify_records = VerifyCode.objects.filter(mobile=self.initial_data['username']).order_by('-add_time')
        if verify_records:
            last_record = verify_records[0]

            five_one_mintes_ago = datetime.now() - timedelta(hours=0,minutes=5,seconds=0)

            if five_one_mintes_ago > last_record.add_time:
                raise serializers.ValidationError('验证码过期')
            if last_record.code != code:
                raise serializers.ValidationError('验证码错误')
        else:
            raise serializers.ValidationError('验证码错误')


    # 作用于整个Serializer,因为user表是没有code字段，所以验证完后需要删除
    # 意思是，整个类表单，会自动View视图函数,？？不存在所以报错？
    # 最后用通过queryset保存
    def validate(self, attrs):
        attrs['mobile'] = attrs['username']
        del attrs['code']

        return attrs


    class Meta:
        model = User
        fields = ('username','code','mobile','password')


class UserDetailSerializer(serializers.ModelSerializer):
    '''
    用户详情的序列化
    '''
    class Meta:
        model = User
        fields = ('name', 'gender', 'birthday','email', 'mobile')