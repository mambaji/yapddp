import requests
import json
import hashlib

create_order_url = 'http://47.112.85.205/channel/pdd/pay'
get_preypay_url = 'http://47.112.85.205/channel/prepay'

app_secret = '73cf4f81-96e4-4ce7-9719-02253a88a9b8'
appid = '9ffd0217-550f-4a25-aabe-19bfbf17e0a5'


def create_order_request():
    sign_params = {
        'appid': appid,
        'out_order_no': 'PT15948632156',
        'amount': '200',
        'pay_code': '1',
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
    }
    paramsStr = sort_sign(sign_params)
    data = {
        'appid': appid,
        'out_order_no': 'PT15948632156',
        'amount': '200',
        'pay_code': '1',
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
        'sign': paramsStr
    }
    print(data)
    resp = requests.post(create_order_url, data=data)
    print(resp.text)
    print(resp.status_code)
    # if(resp.status_code == 200):
    #     pay_url = json.loads(resp.text)
    #     order_sn = pay_url['data']['pay_url'].split(
    #         'http://api.leadnexus.net/pay/')[1]
    #     get_prepay_request(order_sn)


def get_prepay_request(order_sn):
    data = {
        'pay_order': order_sn
    }
    resp = requests.post(get_preypay_url, data=data)
    print(resp.status_code)
    print(resp.text)


def sort_sign(params):
    hl = hashlib.md5()
    sort_params = sorted(params.keys())
    sort_params_str = ''
    for i in sort_params:
        sort_params_str += i+'='+params[i]+'&'
    sort_params_str = sort_params_str[0:-1]
    sort_params_str += app_secret
    print(sort_params_str)
    hl.update(sort_params_str.encode(encoding='utf-8'))
    return hl.hexdigest()


create_order_request()
