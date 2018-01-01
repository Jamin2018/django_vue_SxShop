"""SxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
# from django.contrib import admin
import xadmin
from SxShop.settings import MEDIA_ROOT
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views as AuthView #drf自带token用户认证
from rest_framework_jwt.views import obtain_jwt_token #JWT用户认证
from users.views import SmsCodeViewset ,UserViewset

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


# from goods import views_base
from goods import views
from user_operation.views import UserFavViewset
from user_operation.views import LeavingMessageViewset
from user_operation.views import AddressViewset
from trade.views import ShoppingCarViewset, OrderViewset


#第三方登录后跳转的页面
from django.views.generic import TemplateView


#
# #配合views.py中第六版，后面使用Routers自动配置
# goods_list = views.GoodsListViewSet.as_view({
#     'get':'list',
#     # 'post':'create',
# })

#取代上面，简化配置,配置goods的url
router.register(r'goods',views.GoodsListViewSet,base_name="goods")
#配置catgorys分类
router.register(r'categorys',views.CategoryViewset,base_name="categorys")
#收藏
router.register(r'userfavs',UserFavViewset,base_name="userfavs")

#手机验证
router.register(r'code',SmsCodeViewset,base_name="code")
#手机注册
router.register(r'users',UserViewset,base_name="users")
#留言
router.register(r'messages',LeavingMessageViewset,base_name="messages")
#收货地址
router.register(r'address',AddressViewset,base_name="address")

#购物车
router.register(r'shopcarts',ShoppingCarViewset,base_name="shopcarts")

#订单
router.register(r'orders',OrderViewset,base_name="orders")

#轮播图
router.register(r'banners',views.BannerViewset,base_name="banners")

#主页商品分类数据
router.register(r'indexgoods',views.IndexCategoryViewset,base_name="indexgoods")



urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    #DRF配置
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #图片地址
    url(r'^media/(?P<path>.*)$', serve, {'document_root':MEDIA_ROOT}),

    #商品列表
    # url(r'goods/$',views_base.GoodsListView.as_view(),name='goods-list'),
    #大概前2-5版
    # url(r'goods/$',views.GoodsListViewSet.as_view(),name='goods-list'),
    #第六版
    # url(r'goods/$',goods_list,name='goods-list'),
    #取代后的
    url(r'^',include(router.urls)),

    url(r'docs/',include_docs_urls(title="Jamin生鲜电商")),
    #drf自带token用户登录
    url(r'^api-token-auth/', AuthView.obtain_auth_token),
    #jwt的认证接口
    url(r'^login/$', obtain_jwt_token),

    #第三方登录
    url('', include('social_django.urls', namespace='social')),

    #第三方登录后跳转的页面
    url(r'^index/', TemplateView.as_view(template_name="index.html"), name="index"),
]
