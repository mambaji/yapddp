import requests
import json
import hashlib
import os
import time

create_order_url = 'http://47.112.85.205/channel/pdd/pay'
get_preypay_url = 'http://47.112.85.205/channel/prepay'

app_secret = '721dcd94-7152-4bef-a4c9-fbac083d88e4'
appid = '1f98f01d-3d39-4302-8336-429c08a3768a'
success_num = 0
fail_num = 0


def create_order_request():
    global success_num
    global fail_num
    sign_params = {
        'appid': appid,
        'out_order_no': 'test123456789',
        'amount': '396',
        'pay_code': '1',
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
    }
    paramsStr = sort_sign(sign_params)
    data = {
        'appid': appid,
        'out_order_no': 'test123456789',
        'amount': '396',
        'pay_code': '1',
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
        'sign': paramsStr
    }
    # print(data)
    resp = requests.post(create_order_url, data=data)
    print(resp.text)
    print(resp.status_code)
    # if(json.loads(resp.text)['code'] == 0):
    # pay_url = json.loads(resp.text)['data']['pay_url']
    # os.system(
    #     f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" {pay_url}')

    # print()

    if(resp.status_code == 200):
        success_num += 1
    else:
        fail_num += 1
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


def for_request():
    for i in range(0, 50):
        print(i)
        # time.sleep(0.5)
        create_order_request()
    print(success_num, fail_num)


create_order_request()
# for_request()
