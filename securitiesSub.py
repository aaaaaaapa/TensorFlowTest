import datetime
import json
import random
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from decimal import Decimal
from urllib.parse import urlencode

import requests
import schedule
from chinese_calendar import find_workday
from lxml import etree

from config import verify_str, proxies
from ddddocr import DdddOcr
from login.util import encrypt_pwd
import math
import comm.commPub as com

ocr = DdddOcr()
calc_sum = 0
task_is_run = True
new_bond_list = []
new_bond_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback" \
               "=jQuery1123033795033823781906_1658816743806&sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=10" \
               "&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE" \
               "~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE," \
               "f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO," \
               "f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE," \
               "f23~01~CONVERT_STOCK_CODE~PBV_RATIO&quoteType=0&source=WEB&client=WEB "
login_url = "https://jywg.18.cn/Login/Authentication?validatekey="
verify_url = "http://127.0.0.1:18888/api/verifyUserInfo?"
buy_url = 'https://jywg.18.cn/Trade/Buy'
bond_list_url = 'https://jywg.18.cn/Trade/GetConvertibleBondListV2'
submit_url = 'https://jywg.18.cn/Trade/SubmitBatTradeV2'
new_stk_url = 'https://jywg.18.cn/Trade/QueryNewStkLot?validatekey='
earnings_url = 'https://jywg.18.cn/AccountAnalyze/Api/getPositionSection?v={}&unit=P1Y'
orders_url = 'https://jywg.18.cn/Trade/GetConvertibleBondListV2?validatekey={}'
asset_url = 'https://jywg.18.cn/Com/queryAssetAndPositionV1'
sale_url = 'https://jywg.18.cn/Trade/SubmitTradeV2?validatekey={}'
sale_bond_url = 'https://jywg.18.cn/Search/GetStockList?validatekey={}'
need_trade_url = 'https://jywg.18.cn/Trade/GetAllNeedTradeInfo?validatekey={}'
query_ipo_his_url = 'https://jywg.18.cn/Trade/queryIpoHisMatch?validatekey={}'
asset_acc_url = 'https://jywg.18.cn/Transfer/queryAssetAcc'
payment_of_bond_url = 'https://jywg.18.cn/FundsMgr/StockBankTransferTradeV2?validatekey={}'
ipo_url = 'https://jywg.18.cn/Trade/queryIpoMateNo?validatekey={}'
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36",
    "Content-Type": "application/json"
}
public_key = "-----BEGIN PUBLIC KEY-----\n" + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHdsyxT66pDG4p73yope7jxA92\n" + "c0AT4qIJ/xtbBcHkFPK77upnsfDTJiVEuQDH+MiMeb+XhCLNKZGp0yaUU6GlxZdp\n" + "+nLW8b7Kmijr3iepaDhcbVTsYBWchaWUXauj9Lrhz58/6AE/NF0aMolxIGpsi+ST\n" + "2hSHPu3GSXMdhPCkWQIDAQAB\n" + "-----END PUBLIC KEY----- "
password = ''
auto_exce = False


# 可转债相关操作
# 登录
def login(user_id, pwd):
    req = requests.session()
    login_num = 0
    rand_num = str(random.random())

    # 登录
    while login_num < 10:
        code_url = "https://jywg.18.cn/Login/YZM?randNum={}".format(rand_num)
        code = req.get(code_url, headers=headers, verify=verify_str, proxies=proxies)
        code.encoding = 'utf-8'
        cap = ocr.classification(code.content)

        verify_response = req.get(verify_url + cap, headers=headers, verify=verify_str, proxies=proxies)
        verify_json = json.loads(verify_response.content)

        data = {
            "userId": user_id,
            "password": encrypt_pwd(pwd, public_key),
            'randNumber': rand_num,
            "identifyCode": cap,
            "duration": 30,
            "authCode": "",
            "type": "Z",
            "secInfo": verify_json['userInfo']
        }
        login_response = req.post(login_url, headers=headers, params=data, verify=verify_str, proxies=proxies)
        login_json = json.loads(login_response.content)
        if login_json['Status'] != 0:
            login_num = login_num + 1
        else:
            req.params = {'user_name': login_json['Data'][0]['khmc']}
            return req

    return None


# 获取key
def get_validate_key(req):
    buy = req.get(buy_url, verify=verify_str, proxies=proxies)
    buy.encoding = 'utf-8'
    selector = etree.HTML(buy.text)
    xpath_reg = "//input[@id='em_validatekey']/@value"
    results = selector.xpath(xpath_reg)
    return results[0]


def new_bond(user_id, pwd):
    req = login(user_id, pwd)
    bond_list_response = req.post(bond_list_url, verify=verify_str, proxies=proxies)
    result = json.loads(bond_list_response.content)
    submit_bond_list = []
    if len(result['Data']) > 0:
        for stkData in result['Data']:
            if stkData['ExIsToday']:
                bond = {
                    'StockCode': stkData['SUBCODE'],
                    'StockName': stkData['SUBNAME'],
                    'Price': stkData['PARVALUE'],
                    'Amount': int(stkData['LIMITBUYVOL']),
                    'TradeType': 'B',
                    'Market': stkData['Market']
                }
                submit_bond_list.append(bond)
            else:
                continue

        if len(submit_bond_list) == 0:
            return {'status': 0}
        submit_response = req.post(submit_url, json=submit_bond_list, verify=verify_str, proxies=proxies)
        result = json.loads(submit_response.content)
        return {'status': 1, 'user_id': user_id, 'message': result['Message']}

    else:
        return {'status': 0}


def sale_bond(user_id, pwd):
    req = login(user_id, pwd)
    param = {
        'qqhs': 1000,
        'dwc': ''
    }
    bond_list_response = req.post(sale_bond_url.format(get_validate_key(req)), json=param, verify=verify_str,
                                  proxies=proxies)
    result = json.loads(bond_list_response.content)
    submit_bond_list = []
    if len(result['Data']) > 0:
        for stkData in result['Data']:
            if stkData['Zqlxmc'] == '转换债券' and int(stkData['Zqsl']) >= 10 and float(stkData['Zxjg']) != 100:
                bond = {
                    'stockCode': stkData['Zqdm'],
                    'price': stkData['Zxjg'],
                    'amount': stkData['Zqsl'],
                    'tradeType': 'S',
                    'zqmc': stkData['Zqmc'],
                    'gddm': stkData['Gddm'],
                    'market': stkData['Market']
                }
                submit_bond_list.append(bond)
            else:
                continue

        if len(submit_bond_list) == 0:
            return {'status': 0}
        for item in submit_bond_list:
            need_trade_param = {
                'stockCode': item['stockCode'],
                'price': item['price'],
                'tradeType': 'S',
                'stockName': item['zqmc'],
                'gddm': item['gddm'],
                'market': item['market'],
                'jylb': 'S'
            }
            submit_response = req.post(need_trade_url.format(get_validate_key(req)), json=need_trade_param,
                                       verify=verify_str, proxies=proxies)
            result = json.loads(submit_response.content)
            time.sleep(0.1)
            submit_response = req.post(sale_url.format(get_validate_key(req)), json=item, verify=verify_str,
                                       proxies=proxies)
            result = json.loads(submit_response.content)
            return {'status': 1, 'user_id': user_id, 'user_name': req.params['user_name'],
                    'message': '{}卖出成功'.format(item['zqmc'])}

    else:
        return {'status': 0}


def query_luck(user_id, pwd):
    req = login(user_id, pwd)
    if req is None:
        print(req)
    new_stk_response = req.post(new_stk_url, verify=verify_str, proxies=proxies)
    result = json.loads(new_stk_response.content)
    luck_num = 0
    if len(result['Data']) > 0:
        result_param = []
        for stkData in result['Data']:
            if stkData['Zqsj'] == '0':
                datetime_p = datetime.datetime.strptime(stkData['Zqrq'], '%Y%m%d')
                next_workday = find_workday(3, datetime_p)
                today = datetime.date.today()
                if next_workday >= today >= datetime_p.date():
                    luck_num = luck_num + 1
                    result_param.append({'status': 1, 'user_id': user_id, 'user_name': req.params['user_name'],
                                         'stk_name': stkData['Ssmc'],
                                         'stk_num': stkData['Zqsl'],
                                         'purchase_date': stkData['Wtrq']})

        if luck_num == 0:
            return {'status': 0, 'user_id': user_id, 'stk_name': ''}
        else:
            return result_param
    else:
        return {'status': 0, 'user_id': user_id, 'stk_name': ''}


def query_forget(user_id, pwd):
    req = login(user_id, pwd)
    param = {
        'Ksrq': datetime.datetime(datetime.date.today().year - 5, 1, 1).strftime('%Y-%m-%d'),
        'Jsrq': datetime.date.today().strftime('%Y-%m-%d'),
        'qqhs': 999999,
        'dwc': ''
    }
    ipo_his_response = req.post(query_ipo_his_url.format(get_validate_key(req)), verify=verify_str, proxies=proxies,
                                json=param)
    result = json.loads(ipo_his_response.content)
    forget_num = 0
    if len(result['Data']) > 0:
        result_param = []
        for stkData in result['Data']:
            if int(stkData['Fqsl']) > 0:
                stk_name = stkData['Zqmc']
                if stk_name == '':
                    stk_name = stkData['Zqdm']
                forget_num = forget_num + 1
                result_param.append({'status': 1, 'user_id': user_id, 'user_name': req.params['user_name'],
                                     'stk_name': stk_name,
                                     'stk_num': stkData['Fqsl'],
                                     'purchase_date': stkData['Wtrq']})

        if forget_num == 0:
            return {'status': 0, 'user_id': user_id, 'stk_name': ''}
        else:
            return result_param
    else:
        return {'status': 0, 'user_id': user_id, 'stk_name': ''}


def query_asset(user_id, pwd):
    req = login(user_id, pwd)
    data = {
        'moneyType': "RMB"
    }
    asset_response = req.post(asset_url, data=data, verify=verify_str, proxies=proxies)
    result = json.loads(asset_response.content)
    luck_num = 0
    data = []
    if len(result['Data']) > 0:
        for stkData in result['Data']:
            if len(stkData['positions']) > 0:
                for position in stkData['positions']:
                    if int(position['Zqsl']) > 0:
                        asset = {'Zqmc': position['Zqmc'], 'Zqsl': position['Zqsl'], 'Zxsz': position['Zxsz']}
                        data.append(asset)
                        luck_num = luck_num + 1
                return {'status': 1, 'user_id': user_id, 'data': data}
        if luck_num == 0:
            return {'status': 0, 'user_id': user_id}
    else:
        return {'status': 0, 'user_id': user_id}


def payment_of_bond(user_id, pwd):
    req = login(user_id, pwd)
    asset_param = {
        'Hbdm': '0',
        'NeedBank': '1'
    }
    asset_response = req.post(asset_acc_url, data=asset_param, verify=verify_str, proxies=proxies)
    result = json.loads(asset_response.content)
    data = result['Data'][0]
    kyjy = float(data['Kyzj'])
    if kyjy >= 0:
        return {'status': -1, 'user_id': user_id, 'balance': kyjy}
    amount = math.ceil(abs(kyjy))
    param = {
        'zzlb': '0',
        'zjzh': user_id,
        'yhdm': data['Sfcgyhdm'],
        'moneyType': 'RMB',
        'zzje': amount,
        'zjmm': encrypt_pwd('', public_key),
        'yhmm': encrypt_pwd('', public_key)
    }
    payment_of_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": 'application/x-www-form-urlencoded',
    }
    transfer_response = req.post(payment_of_bond_url.format(get_validate_key(req)), headers=payment_of_headers,
                                 data=urlencode(param), verify=verify_str, proxies=proxies)
    result = json.loads(transfer_response.content)

    if result['Status'] != 0:
        return {'status': -2, 'user_id': user_id, 'balance': 0}
    else:
        return {'status': 1, 'user_id': user_id, 'balance': 0}


def query_balance(user_id, pwd):
    req = login(user_id, pwd)
    asset_param = {
        'Hbdm': '0',
        'NeedBank': '1'
    }
    asset_response = req.post(asset_acc_url, data=asset_param, verify=verify_str, proxies=proxies)
    result = json.loads(asset_response.content)
    data = result['Data'][0]
    kyjy = float(data['Kyzj'])
    return {'status': 1, 'user_id': user_id, 'user_name': req.params['user_name'], 'balance': kyjy}


def annual_revenue(user_id, pwd):
    req = login(user_id, pwd)
    earnings_response = req.get(earnings_url.format(int(time.time())), verify=verify_str, proxies=proxies)
    result = json.loads(earnings_response.content)
    if result.get('Data') is not None:
        gain_profit = Decimal(result['Data'][0]['gainProfit'])
    else:
        gain_profit = 0
    return {'user_id': user_id, 'user_name': req.params['user_name'], 'gain_profit': gain_profit}


def is_new_bond(req, is_today):
    today = datetime.date.today()
    t_2_workday = find_workday(-3,today)

    bond_list_response = req.get(new_bond_url, verify=verify_str, proxies=proxies)
    bond_list_response.encoding = 'utf-8'
    bond_str = str(bond_list_response.content, encoding="utf-8")
    result = json.loads(bond_str[bond_str.index('(') + 1:len(bond_str) - 2])
    new_bond_num = 0
    global new_bond_list
    new_bond_list = []
    for bond in result['result']['data']:
        datetime_p = datetime.datetime.strptime(bond['VALUE_DATE'][0:10], '%Y-%m-%d').date()
        if is_today:
            if datetime_p == today:
                new_bond_list.append(bond['CORRECODE'])
                print("可转债名称：{}，申购日期：{}".format(bond['SECURITY_NAME_ABBR'], bond['VALUE_DATE']))
                new_bond_num = new_bond_num + 1
        else:
            if t_2_workday <= datetime_p < today:
                print("可转债名称：{}，申购日期：{}".format(bond['SECURITY_NAME_ABBR'], bond['VALUE_DATE']))
                new_bond_num = new_bond_num + 1
    if new_bond_num == 0:
        return False
    return True


def is_purchase(user_id, pwd):
    try:
        req = login(user_id, pwd)
        today = datetime.date.today()
        t_2_workday = find_workday(-1, today)
        data = {'qqhs': 999999, 'dwc': '', 'Startdate': t_2_workday.strftime('%Y-%m-%d'),
                'Enddate': today.strftime('%Y-%m-%d'), 'qryType': 0}
        purchase_response = req.post(ipo_url.format(get_validate_key(req)), params=data, verify=verify_str,
                                     proxies=proxies)
        result = json.loads(purchase_response.content)
        purchase_result = []
        if len(result['Data']) > 0:
            stk_names = []
            for stkData in result['Data']:
                purchase_result.append(stkData['Zqdm'])
                stk_names.append(stkData['Zqmc'])
            if len(purchase_result) > 0 and all(purchase_result[i] in new_bond_list for i in range(len(new_bond_list))):
                return {'status': 1, 'user_id': user_id, 'user_name': req.params['user_name'],
                        'stk_name': ','.join(stk_names)}
        return {'status': 0, 'user_id': user_id, 'user_name': req.params['user_name']}
    except Exception as ex:
        print(ex)


def bath_task(select, user_id_list, task):
    global password
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        for user in user_id_list:
            obj = t.submit(task, user['fundaccount'], user['pwd'])
            obj_list.append(obj)

        print_result(select, obj_list)
        print_result_1(select)
        print("账户数量：{}".format(len(user_id_list)))


def print_result(select, obj_list):
    global calc_sum
    print_list = []
    for data in as_completed(obj_list):
        if isinstance(data.result(), list):
            for result in data.result():
                print_list.append(result)
        else:
            print_list.append(data.result())
    if select == 2 or select == 10:
        print_list.sort(key=lambda x: x['stk_name'], reverse=True)
    if select == 3:
        print_list.sort(key=lambda x: x['gain_profit'], reverse=True)
    if select == 6:
        temp_list = []
        for data in print_list:
            if data['status'] == 1:
                if len(data['data']) > 0:
                    for asset in data['data']:
                        temp_list.append({'status': data['status'], 'user_id': data['user_id'], 'Zqmc': asset['Zqmc'],
                                          'Zqsl': asset['Zqsl'],
                                          'Zxsz': asset['Zxsz']})
        print_list = temp_list
        print_list.sort(key=lambda x: (x['Zqmc']), reverse=True)
    if select == 7 or select == 8:
        print_list.sort(key=lambda x: x['balance'], reverse=True)
    if select == 10:
        print_list = list(filter(lambda x: x['status'] == 1, print_list))
        print_list.sort(key=lambda x: x['purchase_date'], reverse=True)
    index = 0
    print_str = []
    for data in print_list:
        index = index + 1
        if select == 1 or select == 5:
            if data['status'] == 0:
                print_str.append('今日无新债')
            if data['status'] == 1:
                print_str.append('资金账号：{}，打新结果：{}'.format(data['user_id'], data['message']))

        if select == 2:

            if data['status'] == 1:
                calc_sum = calc_sum + 1
                user_name = data['user_name']
                if len(user_name) == 2:
                    user_name = user_name + '\u3000'
                luck = "资金账号：{}，姓名：{},中签证券名称：{}，数量：{}，申购日期：{}".format(data['user_id'],
                                                                                        user_name,
                                                                                        data['stk_name'],
                                                                                        data['stk_num'],
                                                                                        data['purchase_date'])
                print_str.append(luck)
                com.luck_list.append(luck)
        if select == 3:
            calc_sum = calc_sum + data['gain_profit']
            print_str.append(
                '资金账号：{}，姓名：{},今年收益：{}'.format(data['user_id'], data['user_name'], data['gain_profit']))
        if select == 4:
            if data['status'] == 0:
                print_str.append("资金账号：{}，姓名：{}，未申购！".format(data['user_id'], data['user_name']))
            if data['status'] == 1:
                calc_sum = calc_sum + 1
                print_str.append("资金账号：{}，姓名：{}，证券名称：{}，申购成功！".format(data['user_id'], data['user_name'],
                                                                                    data['stk_name']))
        if select == 6:
            if data['status'] == 1:
                if int(data['Zqsl']) <= 30:
                    calc_sum = calc_sum + int(data['Zqsl']) / 10
                print_str.append(
                    '{},资金账号：{}，证券名称：{}，持有数量：{}，市值：{}'.format(index, data['user_id'], data['Zqmc'],
                                                                            data['Zqsl'],
                                                                            data['Zxsz']))
        if select == 7:
            calc_sum = calc_sum + data['balance']
            if data['status'] == 1:
                print_str.append(
                    '资金账号：{}，余额：{},{}'.format(data['user_id'], str(data['balance']).ljust(10, ' '), '缴款成功'))
            if data['status'] == -1:
                print_str.append(
                    '资金账号：{}，余额：{},{}'.format(data['user_id'], str(data['balance']).ljust(10, ' '), '无需缴款'))
            if data['status'] == -2:
                print_str.append('资金账号：{}，余额：{},{}'.format(data['user_id'], str(data['balance']).ljust(10, ' '),
                                                                 '当前时间无法缴款'))
            if data['status'] == 0:
                print_str.append(
                    '资金账号：{}，余额：{},{}'.format(data['user_id'], str(data['balance']).ljust(10, ' '), '缴款失败'))
        if select == 8:
            calc_sum = calc_sum + data['balance']
            if data['status'] == 1:
                print_str.append('资金账号：{}，姓名：{}，余额：{}'.format(data['user_id'], data['user_name'],
                                                                      str(data['balance']).ljust(10, ' ')))
        if select == 9:
            if data['status'] == 1:
                calc_sum = calc_sum + 1
                print_str.append('资金账号：{}，姓名：{}，{}'.format(data['user_id'], data['user_name'],
                                                                 data['message']))
        if select == 10:
            if data['status'] == 1:
                calc_sum = calc_sum + int(data['stk_num'])
                print_str.append(
                    "资金账号：{}，姓名：{},中签证券名称：{}，放弃数量：{}，申购日期：{}".format(data['user_id'],
                                                                                         data['user_name'],
                                                                                         data['stk_name'],
                                                                                         data['stk_num'],
                                                                                         data['purchase_date']))
    for pr_item in print_str:
        print(pr_item)
    if select == 2 and auto_exce:
        requests.get(notice_url.format('打新已中签,中签数量：' + str(len(print_str)), '\n'.join(print_str)),
                     proxies=proxies,
                     verify=verify_str)


def print_result_1(select):
    if select == 2:
        print("中签总数量:{}".format(calc_sum))
    if select == 3:
        print("账号总收益：{}".format(calc_sum))
    if select == 4:
        print("申购成功总数量：{}".format(calc_sum))
    if select == 6:
        print("转债数量：{}".format(calc_sum))
    if select == 7 or select == 8:
        print("余额总数：{}".format(calc_sum))
    if select == 9:
        print("卖出转债数量：{}".format(calc_sum))
    if select == 10:
        print("放弃转债数量：{}".format(calc_sum))


def new_bond_task(req, select, user_id_list):
    if is_new_bond(req, True):
        bath_task(select, user_id_list, new_bond)
    else:
        print("今日无新债")


def _main_():
    req = requests.session()
    while True:
        try:
            select = input(
                "0、退出；1、打新债；2、查询中签；3、查询收益；4、查询申购结果；5、自动打新债；6、查询持仓；7、可转债缴款；8、查询余额；9、卖出转债；10、可转债放弃查询\n选择：")
            if select not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'):
                continue
            global calc_sum
            calc_sum = 0
            select = int(select)
            if select == 0:
                break
            # 加载用户
            with open("userIds.txt", "r") as f:
                users = f.readlines()
                f.close()
            user_id_list = []
            temp_pwd = ''
            for user in users:
                user_arr = user.replace('\n', '').split(',')
                if len(user_arr) == 1:
                    user_id = user_arr[0]
                    pwd = temp_pwd
                if len(user_arr) == 2:
                    user_id = user_arr[0]
                    pwd = temp_pwd = user_arr[1]
                user_id_list.append({'fundaccount': user_id, 'pwd': pwd})
            lucky_num = 0
            exec_task(req, select, user_id_list)
        except Exception as ex:
            traceback.print_exc()


def exec_task(req, select, user_id_list):
    if select == 1:
        new_bond_task(req, select, user_id_list)
    if select == 2:
        if is_new_bond(req, False):
            bath_task(select, user_id_list, query_luck)
        else:
            print("最近未打新债")
    if select == 3:
        bath_task(select, user_id_list, annual_revenue)
    if select == 4:
        if is_new_bond(req, True):
            bath_task(select, user_id_list, is_purchase)

    if select == 5:
        schedule_task(req, select, user_id_list)
    if select == 6:
        bath_task(select, user_id_list, query_asset)
    if select == 7:
        bath_task(select, user_id_list, payment_of_bond)
    if select == 8:
        bath_task(select, user_id_list, query_balance)
    if select == 9:
        bath_task(select, user_id_list, sale_bond)
    if select == 10:
        bath_task(select, user_id_list, query_forget)


def schedule_task_new_bond(req, select, user_id_list):
    global task_is_run, auto_exce
    auto_exce = True
    new_bond_task(req, select, user_id_list)
    if is_new_bond(req, False):
        bath_task(2, user_id_list, query_luck)
    else:
        print("最近未打新债")

    task_is_run = True


def schedule_task(req, select, user_id_list):
    # 每天9：30执行

    schedule.every().day.at("09:30").do(schedule_task_new_bond, req, select, user_id_list)
    global task_is_run
    while True:
        if task_is_run:
            task_is_run = False
            print("下次运行时间：{}".format(schedule.next_run()))

        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    _main_()
