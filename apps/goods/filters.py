# -*- coding:utf-8 -*-

import django_filters
from django.db.models import Q

from .models import Goods


#精准查询
class GoodsFilter(django_filters.rest_framework.FilterSet):
    """
    商品的过滤类
    """
    pricemin = django_filters.NumberFilter(name='shop_price', help_text="最低价格",lookup_expr='gte')
    pricemax = django_filters.NumberFilter(name='shop_price', help_text="最高价格",lookup_expr='lte')
    # name = django_filters.CharFilter(name='name',lookup_expr='icontains')   #模糊查询

    # top_category = django_filters.NumberFilter(method='top_category_filter')

    #
    # def top_category_filter(self, queryset, name, value):
    #     return queryset.filter(Q(category_id=value)|Q(category__parent_category_id=value)|Q(category__parent_category__parent_category_id=value))


    class Meta:
        model = Goods
        # fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
        # fields = ['pricemin', 'pricemax','name']   #模糊查询
        fields = ['pricemin', 'pricemax',]