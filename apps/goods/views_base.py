# -*- coding:utf-8 -*-

from django.views.generic.base import View

from goods import models

class GoodsListView(View):
    def get(self,request):
        '''
        通过django的view实现商品列表页
        :param request:
        :return:
        '''
        json_list = []
        goods = models.Goods.objects.all()[:10]

        # #第一种返回json数据,但是不能序列化datatime等数据
        # for good in goods:
        #     json_dict = {}
        #     json_dict['name'] = good.name
        #     json_dict['category'] = good.category.name
        #     json_dict['market_price'] = good.market_price
        #     json_list.append(json_dict)
        #
        # from django.shortcuts import HttpResponse
        # import json
        #
        # return HttpResponse(json.dumps(json_list),content_type='application/json') #必须要指定 content_type='application/json'



        # # 第二种，但是不能序列化ImageFieldFil，会报错
        # from django.forms.models import model_to_dict
        # for good in goods:
        #     json_dict = model_to_dict(good)
        #     json_list.append(json_dict)
        #
        # from django.shortcuts import HttpResponse
        # import json
        #
        # return HttpResponse(json.dumps(json_list),content_type='application/json') #必须要指定 content_type='application/json'


        # 第三种，使用django特殊的序列化，解决第二种情况

        import json
        from django.core import serializers
        json_data = serializers.serialize("json", goods)
        json_data = json.loads(json_data)
        # from django.shortcuts import HttpResponse
        from django.http import HttpResponse, JsonResponse

        # return HttpResponse(json_data,content_type='application/json') #报错，格式有问题
        return JsonResponse(json_data,safe=False) #报错，格式有问题
