import datetime
import json
import sys

import requests

from ddddocr import DdddOcr

ocr = DdddOcr()
req = requests.session()
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/83.0.4103.97 Safari/537.36",
    "Content-Type": "application/json"
}
public_key = "-----BEGIN PUBLIC KEY-----\n" + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHdsyxT66pDG4p73yope7jxA92\n" + "c0AT4qIJ/xtbBcHkFPK77upnsfDTJiVEuQDH+MiMeb+XhCLNKZGp0yaUU6GlxZdp\n" + "+nLW8b7Kmijr3iepaDhcbVTsYBWchaWUXauj9Lrhz58/6AE/NF0aMolxIGpsi+ST\n" + "2hSHPu3GSXMdhPCkWQIDAQAB\n" + "-----END PUBLIC KEY----- "
login_url = "https://jywg.18.cn/Login/Authentication?validatekey="
k_line_url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&ut=fa5fd1943c7b386f172d6893dbfba10b&rtntype=6&secid={}.{}&klt=101&fqt=1'
bond_line_url = 'https://datacenter-web.eastmoney.com/api/data/v1/get?columns=ALL&token=894050c76af8597a853f5b408b759f5d&sortColumns=date&sortTypes=1&source=WEB&reportName=RPTA_WEB_KZZ_LS&filter=(zcode="{}")&pageNumber=1&pageSize=8000'
new_bond_url = "https://datacenter-web.eastmoney.com/api/data/v1/get?sortColumns=PUBLIC_START_DATE&sortTypes=-1&pageSize={}" \
               "&pageNumber={}&reportName=RPT_BOND_CB_LIST&columns=ALL&quoteColumns=f2~01~CONVERT_STOCK_CODE" \
               "~CONVERT_STOCK_PRICE,f235~10~SECURITY_CODE~TRANSFER_PRICE,f236~10~SECURITY_CODE~TRANSFER_VALUE," \
               "f2~10~SECURITY_CODE~CURRENT_BOND_PRICE,f237~10~SECURITY_CODE~TRANSFER_PREMIUM_RATIO," \
               "f239~10~SECURITY_CODE~RESALE_TRIG_PRICE,f240~10~SECURITY_CODE~REDEEM_TRIG_PRICE," \
               "f23~01~CONVERT_STOCK_CODE~PBV_RATIO&quoteType=0&source=WEB&client=WEB "
# 新债配债风险计算

def get_stk_line(stkcode, purchase_date, offset):
    temp = 0
    if stkcode[0] == '6':
        temp = 1
    stkcode_response = req.get(k_line_url.format(temp, stkcode))
    stk_json = json.loads(stkcode_response.content)
    stk_info_list = []
    if len(stk_json['data']) > 0:
        for stk in stk_json['data']['klines']:
            stk_info = str.split(stk, ',')
            data = {
                'curr_date': int(''.join(str.split(stk_info[0], '-'))),
                'first_price': stk_info[1],
                'last_price': stk_info[2],
                'max_price': stk_info[3],
                'min_price': stk_info[4],
                'stk_code': stkcode
            }
            stk_info_list.append(data)

        less_info_list = list(filter(lambda x: x['curr_date'] < purchase_date, stk_info_list))
        last = less_info_list[len(less_info_list) + offset - 1]
        result = list(filter(lambda x: x['curr_date'] >= last['curr_date'], stk_info_list))
        return result


def get_bond_line(stk_code, purchase_date):
    stk_code_response = req.get(bond_line_url.format(stk_code))
    stk_json = json.loads(stk_code_response.content)
    stk_info_list = []
    if len(stk_json['result']['data']) > 0:
        for stk in stk_json['result']['data']:
            data = {
                'curr_date': int(''.join(str.split(stk['DATE'][0:10], '-'))),
                'last_price': stk['FCLOSE'],
                'stk_code': stk_code
            }
            stk_info_list.append(data)

        result = list(filter(lambda x: x['curr_date'] >= purchase_date, stk_info_list))
        return result


def get_old_bond(begin_day, end_day):
    today = datetime.datetime.now().date() + datetime.timedelta(days=-30)
    page_size = 100
    page_number = 1
    new_bond_list = []
    while True:

        bond_list_response = req.get(new_bond_url.format(page_size, page_number))
        bond_list_response.encoding = 'utf-8'
        result = json.loads(bond_list_response.content)

        is_close = False
        for bond in result['result']['data']:
            datetime_p = int(''.join(str.split(bond['VALUE_DATE'][0:10], '-')))

            if begin_day <= datetime_p:
                if datetime_p > end_day:
                    continue
                if datetime_p <= int(''.join(str(today).split('-'))):
                    data = {
                        'stk_code': bond['CONVERT_STOCK_CODE'],
                        'stk_name': bond['SECURITY_NAME_ABBR'],
                        'bond_code': bond['SECURITY_CODE'],
                        'level': bond['RATING'],
                        'guimo': bond['ACTUAL_ISSUE_SCALE'],
                        'bond_price': bond['CURRENT_BOND_PRICE'],
                        'transfer_price': bond['TRANSFER_PRICE'],
                        'first_per_preplacing': bond['FIRST_PER_PREPLACING'],
                        'purchase_date': int(''.join(str.split(bond['VALUE_DATE'][0:10], '-'))),
                        'listing_date': int(''.join(str.split(bond['LISTING_DATE'][0:10], '-'))),
                    }
                    new_bond_list.append(data)
            else:
                is_close = True
        if is_close:
            break
        page_number = page_number + 1
    return new_bond_list


def _main_():
    old_bond_list = get_old_bond(20170101, 20171230)
    result_list = []
    for bond in old_bond_list:
        stk_info_list = get_stk_line(bond['stk_code'], bond['purchase_date'], -1)
        bond_info_list = get_bond_line(bond['bond_code'], bond['listing_date'])
        first_price = float(stk_info_list[0]['last_price'])
        first_bond_price = float(bond_info_list[0]['last_price'])
        if bond['transfer_price'] is None:
            continue
        data = {
            'is_success': 0,
            'index': 0,
            'exce_price': 0,
            'stk_code': bond['stk_code'],
            'stk_name': bond['stk_name'],
            'purchase_date': bond['purchase_date'],
            'level': bond['level'],
            'guimo': bond['guimo'],
            'bond_price': bond['bond_price'],
            'transfer_price': bond['transfer_price'],
            'last_price': first_price,
            'first_per_preplacing': bond['first_per_preplacing'],
            'transfer_premium_ratio': round((first_price / float(bond['transfer_price']) - 1) * 100, 4),
            'first_bond_price': first_bond_price
        }
        for i in range(len(stk_info_list)):
            exce_price = round((float(stk_info_list[i]['last_price']) / first_price - 1) * 100, 4)
            data['index'] = i
            data['exce_price'] = exce_price
            if float(stk_info_list[i]['last_price']) > first_price and 3 < i < len(stk_info_list) - 1:
                data['is_success'] = 1
                break
            if exce_price < -20 or i == len(stk_info_list) - 1:
                data['is_success'] = 0
                break

        result_list.append(data)
    success = 0
    month_list = []
    month_num = 0
    before_month = 0
    result_list.sort(key=lambda x: x['purchase_date'], reverse=True)
    for result in result_list:
        temp = int(str(result['purchase_date'])[4:6])
        if temp != before_month and before_month != 0:
            month_list.append('{}月，可转债数量:{}'.format(before_month, month_num))
            month_num = 0

        before_month = temp
        month_num = month_num + 1
    result_list.sort(key=lambda x: x['is_success'], reverse=True)
    stk_sum = 0
    bond_sum = 0
    for result in result_list:
        # if result['last_price'] < 30:
        #     continue
        if result['is_success'] == 1:
            success = success + 1

        bond_earnings = round((10000 / float(result['last_price'])) * float(result['first_per_preplacing']) / 100 * (
                float(result['first_bond_price']) - 100), 4)
        stk_earnings = round(10000 * float(result['exce_price']) / 100, 4)
        stk_sum = stk_sum + stk_earnings
        bond_sum = bond_sum + bond_earnings
        earnings = round(bond_earnings + stk_earnings, 4)

        print('转债名：{}，申购日期：{}，可配债：{}，收益：{}%,第{}天,等级：{}，发行规模：{},'
              '转债价格：{},转债溢价率：{}%，转股价：{},申购前3日股价：{},每股配售额：{}，首日转债价格：{}，'
              '1万股票收益：{}，配售转债收益：{},总收益：{}'.format(
            result['stk_name'], result['purchase_date'], result['is_success'],
            result['exce_price'], result['index'], result['level'], result['guimo'], result['bond_price'],
            result['transfer_premium_ratio'], result['transfer_price'], result['last_price'],
            result['first_per_preplacing'],
            result['first_bond_price'], stk_earnings, bond_earnings, earnings)
        )
    print("统计转债数量：{}".format(len(result_list)))
    print("统计转债正收益数量数量：{}".format(success))
    print("成功率：{}%".format(round(success / len(result_list) * 100, 4)) if len(result_list) != 0 else 0)
    print('可转债总收益：{}'.format(round(bond_sum, 4)))
    print('股票总收益：{}'.format(round(stk_sum, 4)))
    print('总收益：{}'.format(round(bond_sum + stk_sum, 4)))
    print('每月可转债数量：{}'.format(';'.join(month_list)))
    sys.exit()


if __name__ == '__main__':
    _main_()
