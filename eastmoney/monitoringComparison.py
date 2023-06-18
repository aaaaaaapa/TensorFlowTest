import datetime
import json
import random
import sys
import time
from urllib.parse import urlencode

import requests

from ddddocr import DdddOcr
from login.util import encrypt_pwd
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
old_url = 'http://hkcbm.eastmoney.com/'
code_url = 'https://101.227.99.128:10443/security/getAuthCode'
login_url = 'https://101.227.99.128:10443/security/doLogin?lang=zh_CN'
get_his_url = 'https://101.227.99.128:10443/gmggt_api/routeBusiness/cbm/tradeMonitor/getTradeMonitorHistoryList'
login_old_url = 'http://hkcbm.eastmoney.com/Home/LoginIn'
get_his_url_old = 'http://hkcbm.eastmoney.com/FinancingMonitor/GetTradeMonitorHistoryList?FUND_ACCOUNT=&RISK_TYPE=&BEGINDATE={}&ENDDATE={}&Rows=200&Page=1&_time={}'

public_key = "-----BEGIN PUBLIC KEY-----\n" + 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQUDdkHri8QotAJ/GqIZaxE1Vpv1b04LX3NCX64z3DSrAmL8iSHhimNnwOk0iPgI2TV50IKWjy0wLq+ziyMi27xAFvk8T0U1ma9aAn+qmmeKLNK9r0B9sv7Jvv0bbpA9z8sGChFLdf1V624T6s5xlJR2LD1hVIlG1S1s1cNYN6awIDAQAB\n' + "-----END PUBLIC KEY----- "
ocr = DdddOcr()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
}


def login_new(user_id, pwd):
    req = requests.session()
    login_num = 0
    req.keep_alive = False
    # 登录
    while login_num < 10:
        code = req.post(code_url, headers=headers, json={}, verify=False)
        code.encoding = 'utf-8'
        response = json.loads(code.content)
        cap = ocr.classification(response['data']['pictureCheckCode'])
        print(cap)
        data = {

            "args": {
                "password": encrypt_pwd(pwd, public_key),
                "username": user_id,
                "productEid": 1,
                "timeout": "20",
                "region": "0",
                "pictureCheckCode": cap,
                "pictureCheckKey": response['data']['pictureCheckKey'],
                "url": "/doLogin?lang=zh_CN"
            },
            'header': {
                "deviceId": "Chrome",
                "sysNo": "dchk_omp",
                "traceId": "96ab21433ad83d4a86aa69e7355fb0504f2f",
                "transactionId": "",
                "userMark": ""
            },
            "_t": int(time.time())
        }

        login_response = req.post(login_url, headers=headers, json=data, verify=False)

        login_json = json.loads(login_response.content)
        if login_json['success']:
            headers['dchktoken'] = login_json['data']['accessToken']
            return req
        else:
            login_num = login_num + 1
    return None


def login_old(user_id, pwd):
    req = requests.session()
    home_response = req.get(old_url)
    req_headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
        'Cookie': home_response.headers.get('Set-Cookie')
    }
    data = {
        "userName": user_id,
        "password": pwd,
        "rememberPassword": 0,
        "code": "",
        "t": random.random()

    }

    login_response = req.post(login_old_url, headers=req_headers, data=urlencode(data))
    login_json = json.loads(login_response.content)
    if login_json['IsSuccess']:
        return req
    if login_json['Data']['IsNeedAuthorityCode']:
        raise ValueError('登录失败，需要赑圆验证一下')
    return None


def get_data_new(init_date):
    req = login_new('liujianhua', 'Ljh@152161')
    if req is None:
        print("登录失败")
        return
    data = {
        "args": {
            'beginDate': init_date,
            'current': 1,
            'size': 200,
            'endDate': init_date,
            '_daterange': [init_date, init_date]
        },
        'header': {
            "deviceId": "Chrome",
            "sysNo": "dchk_omp",
            "traceId": "96ab21433ad83d4a86aa69e7355fb0504f2f",
            "transactionId": "",
            "userMark": ""
        },
        "_t": int(time.time())
    }
    response = req.post(get_his_url, headers=headers, json=data, verify=False)
    response_json = json.loads(response.content)
    y_pan_new = []
    buy_sell_new = []
    ratio_big_trade_new = []
    usr_ip_new = []
    for trade_json in response_json['Data']['data']['records']:
        if trade_json['riskType'] == 'Y盘':
            y_pan_new.append(
                '{},{},{}'.format(trade_json['eiDateTime'], trade_json['securityCode'], trade_json['comments']))
        if trade_json['riskType'] == '大量挂盘取消盘':
            buy_sell_new.append(
                '{},{},{},{}'.format(trade_json['eiDateTime'], trade_json['fundAccount'], trade_json['securityCode'],
                                     trade_json['comments']))
        if trade_json['riskType'] == '大比例交易':
            ratio_big_trade_new.append(
                '{},{},{}'.format(trade_json['eiDateTime'], trade_json['securityCode'],
                                  delete_extra_zero(trade_json['comments'])))
        if trade_json['riskType'] == '异国IP登陆':
            arr = str(trade_json['comments']).split(';')
            arr.sort(key=lambda x: x, reverse=True)
            usr_ip_new.append('{},{}'.format(trade_json['fundAccount'], ';'.join(arr)))
    return y_pan_new, buy_sell_new, ratio_big_trade_new, usr_ip_new


def delete_extra_zero(comments):
    comm = float(str(comments).replace('占比百分之', ''))
    comm = str(comm).rstrip('0')
    comm = int(comm.rstrip('.')) if comm.endswith('.') else float(comm)
    return '占比百分之' + str(comm)


def get_data_old(init_date):
    req = login_old('lubiyuan', 'Emlubiyuan@1')
    response = req.get(
        get_his_url_old.format(init_date, init_date,
                               int(time.time())))
    response_json = json.loads(response.content)
    y_pan_old = []
    buy_sell_old = []
    ratio_big_trade_old = []
    usr_ip_old = []
    for row in response_json['Rows']:
        if row['RISK_TYPE'] == 'Y盘':
            y_pan_old.append(
                '{},{},{}'.format(row['EIDATE'], row['SECURITY_CODE'], row['COMMENTS']))
        if row['RISK_TYPE'] == '大量挂盘取消盘':
            buy_sell_old.append(
                '{},{},{},{}'.format(row['EIDATE'], row['FUND_ACCOUNT'], row['SECURITY_CODE'],
                                     row['COMMENTS']))
        if row['RISK_TYPE'] == '大比例交易':
            ratio_big_trade_old.append(
                '{},{},{}'.format(row['EIDATE'], row['SECURITY_CODE'], row['COMMENTS']))
        if row['RISK_TYPE'] == '异国IP登录':
            arr = str(row['COMMENTS']).split(';')
            arr.sort(key=lambda x: x, reverse=True)
            usr_ip_old.append('{},{}'.format(row['FUND_ACCOUNT'], ';'.join(arr)))
    return y_pan_old, buy_sell_old, ratio_big_trade_old, usr_ip_old


def _main_():
    init_date = datetime.date.today().strftime('%Y%m%d')
    y_pan_new, buy_sell_new, ratio_big_trade_new, usr_ip_new = get_data_new(init_date)
    y_pan_old, buy_sell_old, ratio_big_trade_old, usr_ip_old = get_data_old(init_date)
    diff_y_pan = list(set(y_pan_new) - set(y_pan_old))
    diff_buy_sell = list(set(buy_sell_new) - set(buy_sell_old))
    diff_ratio_big_trade = list(set(ratio_big_trade_new) - set(ratio_big_trade_old))
    diff_usr_ip = list(set(usr_ip_new) - set(usr_ip_old))
    print('今日交易监控比对结果：')
    print('总数量{}条；'.format(len(y_pan_new) + len(buy_sell_new) + len(ratio_big_trade_new) + len(usr_ip_new)))
    if len(diff_y_pan) == 0:
        print('Y盘：{}条；'.format(len(y_pan_new)))
    else:
        print('Y盘：新风控{}条,老风控{}条；'.format(len(y_pan_new), len(y_pan_old)))
    if len(diff_buy_sell) == 0:
        print('大量挂盘取消盘：{}条；'.format(len(buy_sell_new)))
    else:
        print('大量挂盘取消盘：新风控{}条,老风控{}条；'.format(len(buy_sell_new), len(buy_sell_old)))
    if len(diff_ratio_big_trade) == 0:
        print('大比例交易：{}条；'.format(len(ratio_big_trade_new)))
    else:
        print('大比例交易：新风控{}条,老风控{}条；'.format(len(ratio_big_trade_new), len(ratio_big_trade_old)))
        for diff in diff_ratio_big_trade:
            if diff in ratio_big_trade_new:
                print('新风控多的数据' + diff)
            if diff in ratio_big_trade_old:
                print('老风控风控多的数据' + diff)
    if len(diff_usr_ip) == 0:
        print('异国IP登陆：{}条；'.format(len(usr_ip_new)))
    else:
        print('异国IP登陆：新风控{}条,老风控{}条；'.format(len(usr_ip_new), len(usr_ip_old)))
        for diff_ip in diff_usr_ip:
            if diff_ip in usr_ip_new:
                print('新风控多的数据' + diff_ip)
            if diff_ip in usr_ip_old:
                print('老风控风控多的数据' + diff_ip)
    sys.exit()


if __name__ == '__main__':
    try:
        _main_()
    except Exception as ex:
        print(ex)
        sys.exit()
