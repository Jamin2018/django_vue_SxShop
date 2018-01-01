# -*- coding:utf-8 -*-
# 云片网短信验证
import requests

class YunPian(object):

    def __init__(self, api_key):
        self.api_key = api_key
        self.singel_send_url = 'https://sms.yunpian.com/v2/sms/single_send.json'

    def send_sms(self, code, mobile):
        parmas = {
            'apikey':self.api_key,
            'mobile':mobile,
            'text':'【Jamin网站】您的验证码是{code}。如非本人操作，请忽略本短信'.format(code=code)
        }
        response = requests.post(self.singel_send_url,data=parmas)

        import json
        re_dict = json.loads(response.text)
        print(re_dict)
        return re_dict

if __name__ == '__main__':
    yun_pian = YunPian('a3ec808b0329b64ff181e1410ca92fbb')
    yun_pian.send_sms('2017','13030103690')