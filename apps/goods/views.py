from django.shortcuts import render

from .serializers import GoodsSerializer, CategorySerializer , BannerSerializer
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

from rest_framework.authentication import TokenAuthentication  #后端单独设置不需要token，前端也可以解决
from .models import Goods, GoodsCategory ,Banner

##主页一级列表关系
from .serializers import IndexGoodsSerizlizer

#!!!设置DRF扩展的缓存机制，提高网站访问速度
from rest_framework_extensions.cache.mixins import CacheResponseMixin

#!!!设置访问限速，减少爬虫的压力
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle

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
    page_size = 12       #默认值
    page_size_query_param = 'page_size'
    page_query_param = 'page'
    max_page_size = 100

# class GoodsListView(generics.ListAPIView):
#     '''
#     第五版，完美返回JASON数据，代码简洁加强版，加深度定制分页
#     '''
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     pagination_class = GoodsPagination  #分页


#CacheResponseMixin  放在最前面，缓存
class GoodsListViewSet(CacheResponseMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    '''
    第六版，完美返回JASON数据，代码简洁加强版，加深度定制分页，动态简便绑定http提交方法：router.register(r'goods',views.GoodsListViewSet),
    搜索、过滤、排序
    '''
    #设置访问限速，记得也要设置setting.py
    throttle_classes = (UserRateThrottle,AnonRateThrottle)

    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination  #分页

    #后端单独设置不需要token，前端也可以解决,因为商品是公开页面，不需要单独设置，故注释掉
    # authentication_classes = (TokenAuthentication, )

    #精确过滤搜索
    filter_backends = (DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter,)
    # filter_fields = ('name', 'shop_price',)
    # 自定义区间定义
    filter_class = GoodsFilter

    #搜索
    search_fields = ('name', 'goods_brief','goods_desc')
    #排序
    ordering_fields = ('sold_num', 'shop_price')



    # 太麻烦，判断条件多的话就麻烦了。将用filter代替
    # def get_queryset(self):
    #     queryset = Goods.objects.all()
    #     price_min = self.request.query_params.get('price_min',0)
    #     if price_min:
    #         queryset = Goods.objects.filter(shop_price__gt=int(price_min))
    #     return queryset

    # 重新写获取商品的详情的代码
    def retrieve(self, request, *args, **kwargs):
        '''
        instance是商品的实例，可以对实例下面的属性进行操作和保存
        '''
        instance = self.get_object()

        #添加了商品阅览数加一
        instance.click_num += 1
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


#标签分类
class CategoryViewset(mixins.ListModelMixin, viewsets.GenericViewSet,mixins.RetrieveModelMixin):
    '''
    商品分类列表数据
    '''
    queryset = GoodsCategory.objects.filter( category_type=1)
    serializer_class = CategorySerializer


#轮播图
class BannerViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    获取轮播图列表
    '''
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer
#主页一级列表关系
class IndexCategoryViewset(mixins.ListModelMixin,viewsets.GenericViewSet):
    '''
    首页商品分类数据
    '''
    queryset = GoodsCategory.objects.filter(is_tab=True,name__in=['生鲜食品','酒水饮料'])
    serializer_class = IndexGoodsSerizlizer