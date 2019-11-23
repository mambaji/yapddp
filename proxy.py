# coding=utf-8
import requests
import json
import os
from data import *
import time
import datetime

# 请求地址
getParamsUrl = "https://mobile.yangkeduo.com/order_checkout.html"
createOrderUrl = "https://mobile.yangkeduo.com/proxy/api/order"
prepayUrl = "https://mobile.yangkeduo.com/proxy/api/order/prepay"

# 代理服务器
proxyHost = "ip"
proxyPort = "port"


proxyMeta = "http://%(host)s:%(port)s" % {

    "host": '58.218.200.228',
    "port": '7683',
}

proxies = {
    "http": proxyMeta,
}

orderList = []
shop_index = 2
goods_index = 2
stock_index = 0


def on_prepay_request(order_sn, type):
    global stock_index
    params = {
        'pdduid': stock[stock_index]['uid']
    }
    data = {
    }
    if(type == 1):
        data = {
            'attribute_fields': {
                'paid_times': 0
            },
            'paid_times': 0,
            'order_sn': order_sn,
            'pap_pay': 1,
            'pay_app_id': 38,
            'version': 3
        }
    else:
        data = {
            'attribute_fields': {
                'paid_times': 0,
                'forbid_contractcode': "1",
                'forbid_pappay': "1"
            },
            'forbid_contractcode': "1",
            'forbid_pappay': '1',
            'paid_times': 0,
            'order_sn': order_sn,
            'pay_app_id': 9,
            'return_url': 'https://mobile.yangkeduo.com/transac_wappay_callback.html?order_sn='+order_sn,
            'version': 3
        }
    headers = {
        'accept ': '*/*',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'accesstoken': stock[stock_index]['token'],
        'content-type': 'application/json;charset=UTF-8',
        'cookie': shop[shop_index]['cookie']+'SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1;msec=1800000;pdd_user_id='+stock[stock_index]['uid']+';PDDAccessToken='+stock[stock_index]['token']+';ua=Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI;webp=1; rec_list_order_detail=rec_list_order_detail_hznLXi'
    }
    resp = requests.post(prepayUrl, headers=headers, params=params,
                         data=json.dumps(data))
    if(resp.status_code == 200):
        t = time.time()
        orderList.append(order_sn)
        print('获取prepayId成功', len(orderList), resp.text)
        stock_index += 1
        if(stock_index >= len(stock)):
            stock_index = 0
        before_get_params()
    else:
        stock_index += 1
        if(stock_index >= len(stock)):
            stock_index = 0
        # print('成功订单数：'+len(orderList))
        print('获取prepayId失败:'+resp.text, stock_index, len(orderList))
        # before_get_params()


def on_get_params_request(shop_cookie, user_id, PDDAccessToken, ua, params):
    cookie = shop_cookie+';pdd_user_id='+user_id+';PDDAccessToken='+PDDAccessToken + \
        ';SL_GWPT_Show_Hide_tmp=1;SL_wptGlobTipTmp=1;rec_list_personal=rec_list_personal_1txxk9;rec_list_index=rec_list_index_erYy8G;ua=' + \
        ua+';webp=1;home_bottom=home_bottom_zpB8Qw;mall_main=mall_main_5RfNjh'
    headers = {
        'accept ': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,/;q=0.8,application/signed-exchange;v=b3',
        'accept-encoding': 'gzip,deflate,br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': cookie
    }
    resp = requests.get(getParamsUrl, params=params,
                        headers=headers, proxies=proxies)
    if(resp.status_code == 200):
        before_create_order(resp.text)


def on_create_order_request(accesstoken, cookie, params, payload):
    global stock_index

    headers = {
        'accesstoken': accesstoken,
        'cookie': cookie
    }
    resp = requests.post(createOrderUrl, headers=headers, params=params,
                         data=json.dumps(payload), proxies=proxies)
    # print(resp.status_code)
    # print(resp.text)
    if(resp.status_code == 200):
        # t = time.time()
        # orderList.append(json.loads(resp.text)['order_sn'])
        # print(stock_index, len(orderList), json.loads(resp.text)
        #       ['order_sn'], int(round(t * 1000)))
        # stock_index += 1
        # if(stock_index >= len(stock)):
        #     stock_index = 0
        on_prepay_request(json.loads(resp.text)['order_sn'], 2)
    else:
        stock_index += 1
        if(stock_index >= len(stock)):
            stock_index = 0
        # print('成功订单数：'+len(orderList))
        print('创建订单失败:'+resp.text, stock_index, len(orderList))
        before_get_params()
    # before_create_order(resp.text)


def before_get_params():
    ua = 'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI;'
    params = {
        'sku_id': goods[goods_index]['sku_id'],
        'group_id': goods[goods_index]['group_id'],
        'goods_id': goods[goods_index]['goods_id'],
        'goods_number': 1,
        'showwxpaytitle': 1,
        'refer_page_element': 'open_btn',
        'source_channel': 0,
        'refer_page_name': 'goods_detail'
    }
    on_get_params_request(shop[shop_index]['cookie'], stock[stock_index]
                          ['uid'], stock[stock_index]['token'], ua, params)


def before_create_order(text):
    ua = 'Mozilla/5.0 (Linux; U; Android 4.1.2; zh-cn; Chitanda/Akari) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 MicroMessenger/6.0.0.58_r884092.501 NetType/WIFI;'
    cookie = shop[shop_index]['cookie']+';pdd_user_id='+stock[stock_index]['uid']+';PDDAccessToken='+stock[stock_index]['token']+';ua='+ua + \
        ';promotion_subject=promotion_subject_XzgWTD;webp=1;msec=1800000;rec_list_order_detail=rec_list_order_detail_OPiDpF'
    params = {
        'pdduid': stock[stock_index]['uid']
    }
    dictObj = fix_html(text)
    anti_content = os.popen(f"node merge.js").read().strip()
    data = {
        "address_id": dictObj['store']['addressInfo']['addressId'],
        "goods": [
            {
                "sku_id": dictObj['store']['skuId'],
                "sku_number": dictObj['store']['goodsInfo']['number'],
                "goods_id": dictObj['store']['goodsId']
            }
        ],
        "group_id": dictObj['store']['groupId'],
        "anti_content": anti_content,
        "page_from": 0,
        "activity_id": None,
        "duoduo_type": 0,
        "biz_type": 0,
        "attribute_fields": {
            "create_order_token": dictObj['store']['extendMap']['create_order_token'],
            "create_order_check": dictObj['store']['extendMap']['create_order_check'],
            "original_front_env": 0,
            "current_front_env": 1,
            "PTRACER-TRACE-UUID": dictObj['store']['extendMap']['PTRACER-TRACE-UUID']
        },
        "source_channel": "0",
        "source_type": 0,
        "pay_app_id": -1,
        "is_app": "0",
        "vsion": 1
    }
    on_create_order_request(stock[stock_index]['token'], cookie, params, data)


def fix_html(text):
    list = text.split('rawData=')
    index = list[1].find(';')
    jsontext = list[1][0:index]
    # print(list[1])
    value = json.loads(jsontext)
    return value


def main():
    before_get_params()


main()
