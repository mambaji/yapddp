import requests
import json
import hashlib
import os
import time
import datetime

create_order_url = 'http://47.112.85.205/channel/pdd/pay'
get_preypay_url = 'http://47.112.85.205/channel/prepay'
call_back_url = 'http://47.112.85.205/dock/callback'
# app_secret = input('请输入商户Sercet:')
# appid = input('请输入商户appId：')
# goodPrice = input('请输入商品价格：')
# for_num = int(input('请输入下单数：'))
# pay_code = input('请输入支付类型：1 微信支付、2 支付宝支付')

app_secret = '6b330855-6d06-443f-ae33-dcd6adda3c3e'
appid = 'e1a45822-7d8a-4ccc-ba49-6e48bd4f3873'
dock_appid = 'fdc970b5-19d9-4320-839e-e33b720adb85'
dock_secret = '6868f9b8-72de-4d31-b2ad-4ac7f8dac036'
goodPrice = '297'
for_num = 10
pay_code = '2'

success_num = 0
fail_num = 0


def create_order_request(order):
    global success_num
    global fail_num
    sign_params = {
        'appid': appid,
        'out_order_no': order,
        'amount': goodPrice,
        'pay_code': pay_code,
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
    }
    paramsStr = sort_sign(sign_params, app_secret)
    data = {
        'appid': appid,
        'out_order_no': order,
        'amount': goodPrice,
        'pay_code': pay_code,
        'notify_url': 'http://47.112.85.205/test/callback',
        'return_url': 'https://www.baidu.com',
        'sign': paramsStr
    }
    resp = requests.post(create_order_url, data=data, timeout=5)
    print(resp.text)

    # if(json.loads(resp.text)['code'] == 0):
    # pay_url = json.loads(resp.text)['data']['pay_url']
    # os.system(
    #     f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" {pay_url}')
    if(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        success_num += 1
        print('创建成功', json.loads(resp.text)['data']['pay_url'])
        call_back(order, json.loads(resp.text)['data']['sys_order_no'])
    else:
        fail_num += 1
        print('创建失败', resp.status_code, resp.text)
    # if(resp.status_code == 200):
    #     pay_url = json.loads(resp.text)
    #     order_sn = pay_url['data']['pay_url'].split(
    #         'http://api.leadnexus.net/pay/')[1]
    #     get_prepay_request(order_sn)


def get_prepay_request(order_sn):
    data = {
        'pay_order': order_sn
    }
    resp = requests.post(get_preypay_url, data=data, timeout=5)
    # print(resp.status_code)
    # print(resp.text)


def call_back(out_order_no, sys_order_no):
    data = {
        'appid': dock_appid,
        'out_order_no': sys_order_no,
        'sys_order_no': out_order_no,
    }
    signstr = sort_sign(data, dock_secret)
    data['sign'] = signstr
    print(data)
    resp = requests.post(call_back_url, data=data, timeout=5)
    print(resp.status_code, resp.text)


def sort_sign(params, secret):
    hl = hashlib.md5()
    sort_params = sorted(params.keys())
    sort_params_str = ''
    for i in sort_params:
        sort_params_str += i+'='+params[i]+'&'
    sort_params_str = sort_params_str[0:-1]
    sort_params_str += secret
    hl.update(sort_params_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def for_request():
    global success_num, fail_num
    for i in range(0, for_num):
        create_order_request()
    print('创建订单结束：')
    print('总共创建'+str(success_num+fail_num)+',成功次数：' +
          str(success_num)+',失败次数：'+str(fail_num))


t = time.time()
create_order_request('test'+str(int(round(t * 1000))))

# for_request()
