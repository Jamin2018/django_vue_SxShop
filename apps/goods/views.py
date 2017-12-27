from django.shortcuts import render

from .serializers import GoodsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import status   #post后返回的http信息，加装后的功能，不清楚的看源码
from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

from rest_framework import viewsets   #最终最好用的
from django_filters.rest_framework import DjangoFilterBackend  #精确搜索
from .filters import GoodsFilter  #自定义精确范围搜索
from rest_framework import filters

from .models import Goods
# Create your views here.

# # 第一版，完美返回JASON数据
# class GoodsListView(APIView):
#     '''
#     第一版，完美返回JASON数据
#     '''
#     def get(self,request,format = None):
#         goods = Goods.objects.all()[:10]
#         goods_serializer = GoodsSerializer(goods,many = True)   #类似django的form表单使用，many = True表示goods是  QuerySet对象
#         return Response(goods_serializer.data)
#
#     # 前端没有提供接口，注释了
#     # def post(self,request):
#     #     #类似django自带的form表单验证
#     #     serializer = GoodsSerializer(data=request.data)   #封装后有了request.data属性，原django表单是没有的
#     #     if serializer.is_valid():
#     #         serializer.save()  #调用该函数的create方法
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # 第二版，完美返回JASON数据，加强版
# class GoodsListView(mixins.ListModelMixin,
#                     generics.GenericAPIView,
#                    ):
#     '''
#     第二版，完美返回JASON数据，加强版
#     '''
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
#
# # 第三版，完美返回JASON数据，代码简洁加强版
# class GoodsListView(generics.ListAPIView):
#     '''
#     第三版，完美返回JASON数据，代码简洁加强版
#     '''
#     # generics.ListAPIView已经继承了：
#     # mixins.ListModelMixin,
#     # generics.GenericAPIView，
#     # 和
#     # def get(self, request, *args, **kwargs):
#     #     return self.list(request, *args, **kwargs)
#     queryset = Goods.objects.all()[:10]
#     serializer_class = GoodsSerializer

# 第四版，完美返回JASON数据，代码简洁加强版，加分页
# class GoodsListView(generics.ListAPIView):
#     '''
#     第四版，完美返回JASON数据，代码简洁加强版，加分页
#     '''
#     # generics.ListAPIView已经继承了：
#     # mixins.ListModelMixin,
#     # generics.GenericAPIView，
#     # 和
#     # def get(self, request, *args, **kwargs):
#     #     return self.list(request, *args, **kwargs)
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer


#深度定制分页
class GoodsPagination(PageNumberPagination):
    '''
    页面手动添加page_size,如http://127.0.0.1:8000/goods/?p=1&page_size=15,可前端自己定义显示数量
    '''
    page_size = 5       #默认值
    page_size_query_param = 'page_size'
    page_query_param = 'p'
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     '''
#     第五版，完美返回JASON数据，代码简洁加强版，加深度定制分页
#     '''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination  #分页

class GoodsListViewSet(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    第六版，完美返回JASON数据，代码简洁加强版，加深度定制分页，动态简便绑定http提交方法：router.register(r'goods',views.GoodsListViewSet),
    搜索、过滤、排序
    '''
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  #分页
    #精确过滤搜索
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    # filter_fields = ('name', 'shop_price',)
    # 自定义区间定义
    filter_class = GoodsFilter

    #搜索
    search_fields = ('name', 'goods_brief','goods_desc')
    #排序
    ordering_fields = ('sold_num', 'add_time')



    # 太麻烦，判断条件多的话就麻烦了。将用filter代替
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min',0)
    #     if price_min:
    #         queryset = Goods.objects.filter(shop_price__gt=int(price_min))
    #     return queryset