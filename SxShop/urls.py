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

from rest_framework.routers import DefaultRouter

router = DefaultRouter()


# from goods import views_base
from goods import views

#
# #配合views.py中第六版，后面使用Routers自动配置
# goods_list = views.GoodsListViewSet.as_view({
#     'get':'list',
#     # 'post':'create',
# })

#取代上面，简化配置,配置goods的url
router.register(r'goods',views.GoodsListViewSet,base_name="goods")

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
]
