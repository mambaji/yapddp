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
goodPrice = '1.00'
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
        'notify_url': 'http://47.112.85.205/dock/callback',
        'return_url': 'http://localhost:8089/dpay/idx/ok',
    }
    paramsStr = sort_sign(sign_params, app_secret)
    data = {
        'appid': appid,
        'out_order_no': order,
        'amount': goodPrice,
        'pay_code': pay_code,
        'notify_url': 'http://47.112.85.205/dock/callback',
        'return_url': 'http://localhost:8089/dpay/idx/ok',
        'sign': paramsStr
    }
    print(data)
    resp = requests.post(create_order_url, data=data)
    print(resp.text)

    # if(json.loads(resp.text)['code'] == 0):
    # pay_url = json.loads(resp.text)['data']['pay_url']
    # os.system(
    #     f'"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe" {pay_url}')
    if(resp.status_code == 200 and json.loads(resp.text)['code'] == 0):
        success_num += 1
        print('创建成功', json.loads(resp.text)['data']['pay_url'], json.loads(
            resp.text)['data']['sys_order_no'])
        # call_back(order, json.loads(resp.text)['data']['sys_order_no'])
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


def call_back(sys_order_no, out_order_no):
    data = {
        'appid': dock_appid,
        'out_order_no': out_order_no,
        'sys_order_no': sys_order_no,
    }
    signstr = sort_sign(data, dock_secret)
    data['sign'] = signstr
    print(data)
    resp = requests.post(call_back_url, data=json.dumps(data), timeout=5)
    print(resp.status_code, resp.text)


def sort_sign(params, secret):
    hl = hashlib.md5()
    sort_params = sorted(params.keys())
    print(sort_params)
    sort_params_str = ''
    for i in sort_params:
        sort_params_str += i+'='+params[i]+'&'
    sort_params_str = sort_params_str[0:-1]
    sort_params_str += secret
    print('待签名串', sort_params_str)
    hl.update(sort_params_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def sort_sign_t(params, secret):
    hl = hashlib.md5()
    # sort_params = sorted(params.keys())
    sort_params = params
    print(sort_params)
    sort_params_str = ''
    for i in sort_params:
        sort_params_str += params[i]+'.'
    sort_params_str = sort_params_str[0:-1]
    sort_params_str += secret
    print('待签名串', sort_params_str)
    hl.update(sort_params_str.encode(encoding='utf-8'))
    return hl.hexdigest()


def for_request():
    global success_num, fail_num
    for i in range(0, for_num):
        create_order_request()
    print('创建订单结束：')
    print('总共创建'+str(success_num+fail_num)+',成功次数：' +
          str(success_num)+',失败次数：'+str(fail_num))


def create_order_request_other(order):
    url = "https://pay.lingdupay.com/api/createOrder.htm"
    sercet = "54b25c26d462a049a919a948d4d11d4a"
    parter = "19867211394"
    type = "AG_UNI_FACE"
    price = "199.00"
    global success_num
    global fail_num
    sign_params = {
        'out_trade_no': order,
        'total_fee': price,
        'user_no': parter,
    }
    paramsStr = sort_sign_t(sign_params, sercet)
    print(paramsStr)
    data = {
        'user_no': parter,
        'type': type,
        'total_fee': price,
        'out_trade_no': order,
        # 'callbackurl': 'http://47.112.85.205/dock/callback',
        'sign': paramsStr
    }
    print(data)
    resp = requests.post(url, data=json.dumps(data), timeout=5)
    resp.encoding = 'utf-8'
    print(resp.text)


def call_back_other(orderid):
    data = {
        'orderid': orderid,
        'opstate': '200',
        'value': '400.00',
        'sysorderid': '1554418929',
        'systime': out_order_no,
        'attach': sys_order_no,
        'msg': 'huitiao'
    }
    signstr = sort_sign(data, dock_secret)
    data['sign'] = signstr
    print(data)
    resp = requests.post(call_back_url, data=json.dumps(data), timeout=5)
    print(resp.status_code, resp.text)


t_sign_params = {
    'parter': '8074',
    'type': '1006',
    'value': '199.00',
    'orderid': 'sys-dock-1577453928450751320',
    'callbackurl': 'http://47.112.85.205/dock/callback',
}
print(sort_sign_t(t_sign_params, '01379c339eac46bda2e9b70d167d2cad'))
t = time.time()
# create_order_request_other('test'+str(int(round(t * 1000))))
create_order_request('test'+str(int(round(t * 1000))))

# for_request()
