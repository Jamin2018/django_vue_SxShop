# -*- coding:utf-8 -*-
#类似于django自带的form表单验证
from rest_framework import serializers

from goods import models

#第一种，类form表单
# class GoodsSerializer(serializers.Serializer):
#     name = serializers.CharField(required=True,max_length=300)
#     click_num = serializers.IntegerField(default=0)
#     goods_front_image = serializers.ImageField()
#
#     #保存
#     def create(self, validated_data):
#
#         return models.Goods.objects.create(**validated_data)
#
# # 第二种，简化加强版类form表单
# class GoodsSerializer(serializers.ModelSerializer):
#     category = CategorySerilizer
#     class Meta:
#         model = models.Goods
#         # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
#         fields = "__all__"          #所有字段



# 获取上面传递的category外键所对应的数据的所有信息,并添加到GoodsSerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsCategory
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段


# 第二种，简化加强版类form表单
# 嵌套信息需要放在下面
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = models.Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段