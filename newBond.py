import datetime
import json
import random
import sys
import time
from decimal import Decimal

import requests
from chinese_calendar import find_workday
from lxml import etree

from ddddocr import DdddOcr
from login.util import encrypt_pwd



def _main_():
    today = datetime.date.today()
    t_2_workday = find_workday(-2, today)
    ocr = DdddOcr()
    rand_num = str(random.random())
    # ssl._create_default_https_context = ssl._create_unverified_context
    req = requests.session()
    new_bond_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?callback" \
                   "=jQuery1123033795033823781906_1658816743806&sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize=10" \
                   "&pageNumber=1&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE" \
                   "~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE," \
                   "f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO," \
                   "f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE," \
                   "f23~01~CONVERT_STOCK_CODE~PBV_RATIO&quoteType=0&source=WEB&client=WEB "
    login_url = "https://jywg.18.cn/Login/Authentication?validatekey="

    code_url = "https://jywg.18.cn/Login/YZM?randNum={}".format(rand_num)
    buy_url = 'https://jywg.18.cn/Trade/Buy'
    bond_list_url = 'https://jywg.18.cn/Trade/GetConvertibleBondListV2?validatekey='
    submit_url = 'https://jywg.18.cn/Trade/SubmitBatTradeV2'
    new_stk_url = 'https://jywg.18.cn/Trade/QueryNewStkLot?validatekey='
    earnings_url = 'https://jywg.18.cn/AccountAnalyze/Api/getPositionSection?v={}&unit=Y'
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/83.0.4103.97 Safari/537.36",
        "Content-Type": "application/json"
    }
    public_key = "-----BEGIN PUBLIC KEY-----\n" + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHdsyxT66pDG4p73yope7jxA92\n" + "c0AT4qIJ/xtbBcHkFPK77upnsfDTJiVEuQDH+MiMeb+XhCLNKZGp0yaUU6GlxZdp\n" + "+nLW8b7Kmijr3iepaDhcbVTsYBWchaWUXauj9Lrhz58/6AE/NF0aMolxIGpsi+ST\n" + "2hSHPu3GSXMdhPCkWQIDAQAB\n" + "-----END PUBLIC KEY-----"
    gain_profit_sum = 0
    # 选择
    while True:
        select = input("0、退出；1、打新债；2、查询中签；3、查询收益；4、自动打新债；\n选择：")
        if select not in ('0', '1', '2', '3','4'):
            continue
        if select == '0':
            break
        lucky_num = 0
        if select == '2':
            # 判断T-2日是否有新债
            bond_list_response = req.get(new_bond_url, headers=headers)
            bond_list_response.encoding = 'utf-8'
            bond_str = str(bond_list_response.content, encoding="utf-8")
            result = json.loads(bond_str[bond_str.index('(') + 1:len(bond_str) - 2])
            new_bond_num = 0
            for bond in result['result']['data']:
                datetime_p = datetime.datetime.strptime(bond['VALUE_DATE'][0:10], '%Y-%m-%d').date()
                if t_2_workday <= datetime_p < today:
                    new_bond_num = new_bond_num + 1
                    # print("可转债名称：{}，申购日期：{}".format(bond['SECURITY_NAME_ABBR'], bond['VALUE_DATE']))
            if new_bond_num == 0:
                print("最近未打新债")
                continue
        if select == '3':
            gain_profit_sum = 0
        with open("userIds.txt", "r") as f:
            user_id_list = f.readlines()
            f.close()
        for user_id in user_id_list:
            user_id = user_id.replace('\n', '')
            login_num = 0
            cookies = ''
            # 登录
            while login_num < 100:
                code = req.get(code_url, headers=headers)
                code.encoding = 'utf-8'

                cap = ocr.classification(code.content)

                data = {
                    "userId": user_id,
                    "password": encrypt_pwd('623392', public_key),
                    'randNumber': rand_num,
                    "identifyCode": cap,
                    "duration": 30,
                    "authCode": "",
                    "type": "Z"
                }

                login = req.post(login_url, headers=headers, params=data)
                login_json = json.loads(login.content)
                if login_json['Status'] != 0:
                    login_num = login_num + 1
                else:
                    cookies = login.cookies
                    break
            # if login_num > 0:
            #     print("资金账号：{}，登录成功，登录失败次数：{}".format(userId, login_num))
            # 获取validateKey
            buy = req.get(buy_url, cookies=cookies, headers=headers)
            buy.encoding = 'utf-8'
            selector = etree.HTML(buy.text)
            xpath_reg = "//input[@id='em_validatekey']/@value"
            results = selector.xpath(xpath_reg)
            validate_key = results[0]
            validate_data = {
                'validatekey': validate_key
            }
            # 打新
            if select == '1':
                bond_list_response = req.post(bond_list_url + validate_key, params=validate_data, cookies=cookies,
                                              headers=headers)
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
                        print("今日无新债")
                        break
                    submit_response = req.post(submit_url, json=submit_bond_list)
                    result = json.loads(submit_response.content)
                    msg = "时间：{}，资金账号：{}，打新结果：{}".format(datetime.datetime.now(), user_id, result['Message'])
                    print(msg)
                    with open("log.txt", "a") as f:
                        f.write(msg + '\n')
                        f.close()
                    lucky_num = lucky_num + 1

                else:
                    print("今日无新债")
                    break
            # 查询中签证券
            if select == '2':
                new_stk_response = req.post(new_stk_url + validate_key, params=validate_data)
                result = json.loads(new_stk_response.content)
                if len(result['Data']) > 0:
                    for stkData in result['Data']:
                        if stkData['Zqsj'] == '0':
                            datetime_p = datetime.datetime.strptime(stkData['Zqrq'], '%Y%m%d')
                            next_workday = find_workday(1, datetime_p)
                            today = datetime.date.today()
                            if next_workday >= today >= datetime_p:
                                print("资金账号：{}，中签证券名称：{}，申购日期：{}".format(user_id, stkData['Ssmc'], stkData['Wtrq']))
                                lucky_num = lucky_num + 1
                else:
                    print("资金账号：{}，未中签！".format(user_id))
            # 查询新债年收益
            if select == '3':
                earnings_response = req.get(earnings_url.format(int(time.time())))
                result = json.loads(earnings_response.content)
                if result.get('Data') is not None:
                    gain_profit = Decimal(result['Data'][0]['gainProfit'])
                    gain_profit_sum = gain_profit_sum + gain_profit
                    print('资金账号：{}，今年收益：{}'.format(user_id, gain_profit))
                else:
                    print('资金账号：{}，今年收益：{}'.format(user_id, 0))
            time.sleep(random.uniform(0.01, 0.03))
        if select == '2':
            print("中签数量：{}".format(str(lucky_num)))
        if select == '1':
            print("打新数量：{}".format(str(lucky_num)))
        if select == '3':
            print("账号总收益：{}".format(gain_profit_sum))
    sys.exit()


if __name__ == '__main__':
    _main_()

