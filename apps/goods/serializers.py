# -*- coding:utf-8 -*-
#类似于django自带的form表单验证
from rest_framework import serializers

from goods import models

from django.db.models import Q

#第一种，类form表单，自己写验证，用户购物车那里使用了
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


#第三类
class CategorySerializer3(serializers.ModelSerializer):

    class Meta:
        model = models.GoodsCategory
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段


#第二类
class CategorySerializer2(serializers.ModelSerializer):
    #因为外键是自己，所以要用到反向关联键
    #sub_cat 是指定的反向关联键
    sub_cat = CategorySerializer3(many=True)  # 下面有多个2类，一定要加 many=True
    class Meta:
        model = models.GoodsCategory
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段


#第一类
# 获取上面传递的category外键所对应的数据的所有信息,并添加到GoodsSerializer
class CategorySerializer(serializers.ModelSerializer):
    '''
    商品分类序列化
    '''
    #因为外键是自己，所以要用到反向关联键
    #sub_cat 是指定的反向关联键
    sub_cat = CategorySerializer2(many=True)   #下面有多个2类，一定要加 many=True
    class Meta:
        model = models.GoodsCategory
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段

#加入图片到Goods中
class GoodsImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsImage
        fields =  ('image',)


# 第二种，简化加强版类form表单
# 嵌套信息需要放在下面
class GoodsSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    #images 反向关联的键
    images = GoodsImageSerializer(many=True)
    class Meta:
        model = models.Goods
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        # fields = ('name', 'click_num', 'market_price', 'add_time', )  #指定字段
        fields = "__all__"          #所有字段


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.GoodsCategoryBrand
        fields = "__all__"  # 所有字段


#主页一级列表关系
class IndexGoodsSerizlizer(serializers.ModelSerializer):
    brands = BrandSerializer(many=True)
    #因为需要第二级的分类，因为商品属于第三级分类，所以下面这个不符合
    # goods = GoodsSerializer()
    # 所以下面自己查询
    goods = serializers.SerializerMethodField()

    sub_cat = CategorySerializer2(many=True)
    #同上
    ad_goods = serializers.SerializerMethodField()


    #因为需要第二级的分类，因为商品属于第三级分类，所以下面这个不符合
    # goods = GoodsSerializer()
    # 所以下面自己查询
    def get_goods(self,obj):
        all_goods = models.Goods.objects.filter(Q(category_id=obj.id)|Q(category__parent_category_id=obj.id)|Q(category__parent_category__parent_category_id=obj.id))
        # 所以需要加  context={'request':self.context['request']}  这个参数
        goods_serializer = GoodsSerializer(all_goods,many=True,context={'request':self.context['request']} )  #序列化查到的数据
        return goods_serializer.data

    #同上
    def get_ad_goods(self,obj):
        goods_json = {}
        ad_goods = models.IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            goods_ins = ad_goods[0].goods
            # 在Serizlizer重新定制Serizlizer，返回的图片就没有加域名
            # 因为自己定制不会自动传入下面参数，需要手动传
            # 所以需要加  context={'request':self.context['request']}  这个参数
            goods_json = GoodsSerializer(goods_ins,many=False,
                                         context={'request':self.context['request']}).data   #上面为什么是Ture，下面为什么是False
            # 可能是这里查到的goods_ins是一个，上面查到的all_goods可能是多个
        return goods_json

    class Meta:
        model = models.GoodsCategory
        fields = "__all__"          #所有字段
