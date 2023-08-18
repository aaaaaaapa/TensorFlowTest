import datetime
import json
import sys
import time
import traceback
import random

import requests
import schedule
from chinese_calendar import is_holiday
from pandas import DataFrame

from config import proxies, verify_str

login_url = "http://m.quyundong.com/login/dologin"
goods_id_url = "http://m.quyundong.com/court/book?bid=22377&t={}&cid=1"
confirm_url = "http://m.quyundong.com/order/Confirm?{}&allcourse_name=A%E5%8F%B7%E5%9C%BA%2CB%E5%8F%B7%E5%9C%BA%2CC%E5%8F%B7%E5%9C%BA%2CD%E5%8F%B7%E5%9C%BA%2C&goods_ids={}&book_date={}&court_name=%E4%B8%8A%E6%B5%B7%E5%B8%82%E5%BE%90%E6%B1%87%E5%8C%BA%E9%9D%92%E5%B0%91%E5%B9%B4%E6%B0%B4%E4%B8%8A%E8%BF%90%E5%8A%A8%E5%AD%A6%E6%A0%A1&category_name=%E7%BE%BD%E6%AF%9B%E7%90%83&bid=22377&cid=1&order_type=0&relay=0&token={}"
confirm_do_url = "https://m.quyundong.com/order/doconfirm?goods_ids={}&act_id=0&code=0&bid=22377&cid=1&coupon_id=0&ticket_type=0&utm_source=&pay_type=&card_no=&relay=0&package_type=0&hash={}&sale_list=%7B%7D&invoice_id=0&_={}&token={}"
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'

url_param = "price%5B%5D={}&hour%5B%5D={}&course_name%5B%5D={}%E5%8F%B7%E5%9C%BA&real_time%5B%5D={}%3A00-{}%3A00"
task_is_run = True
req = requests.session()
username = '17301706429'
password = 'zx2651yf'
sit_times = [19, 20, 21]
holiday_sit_times = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
work_sit_times = [19, 20, 21]
init_date = datetime.datetime.today()
court_num = 2
goods_info = None
pickup_days = 6


def _main_():
    global username, password, sit_times, holiday_sit_times, court_num, work_sit_times
    with open("quyundong.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    if len(configList) != 6:
        print('配置文件错误！')
        input('输入任意键退出')
        sys.exit()
    for config in configList:
        if config.startswith('用户名'):
            username = config.replace('\n', '').split('=')[1].split(',')[0]
        if config.startswith('密码'):
            password = config.replace('\n', '').split('=')[1].split(',')[0]
        if config.startswith('场地数量'):
            court_num = config.replace('\n', '').split('=')[1].split('-')[0]
        if config.startswith('时间段'):
            name_str = config.replace('\n', '').split('=')[1]
            if name_str != '':
                work_sit_times = name_str.split(',')
        if config.startswith('假日时间段'):
            name_str = config.replace('\n', '').split('=')[1]
            if name_str != '':
                holiday_sit_times = name_str.split(',')
        if config.startswith('抢票时间'):
            exec_time = config.replace('\n', '').split('=')[1]

    # exec_time = "00:06"
    schedule_task(exec_time)
    # login()
    # client_task()


def client_task():
    for i in range(120):
        task()
        if goods_info is not None:
            break
        randint_time = random.randint(20 * 1000, 35 * 1000)
        print("等待{}毫秒继续搜索~".format(randint_time))
        time.sleep(randint_time / 1000)


def task():
    global task_is_run, init_date, goods_info, sit_times

    init_date = datetime.datetime.today() + datetime.timedelta(days=pickup_days)
    # sit_times = holiday_sit_times
    if is_holiday(init_date):
        sit_times = holiday_sit_times
    else:
        sit_times = work_sit_times
    print('当前时间：{}'.format(datetime.datetime.now()))
    start = time.perf_counter()
    goods_result = get_goods_result()
    end = time.perf_counter()
    print('加载goods数据耗时：{:.4f}s'.format(end - start))
    index_arr = []
    index = 0
    goods_arr = []
    while True:
        index = goods_result.find('available', index + 1)
        if index == -1:
            break
        index_arr.append(index)
    for index in index_arr:
        r_index = goods_result[0:index].rfind('course_content')
        sit_time = goods_result[r_index:index].split(',')[1]
        number = goods_result[r_index + 16:r_index + 17]
        goods_index = goods_result[0:r_index].rfind('goodsid')
        goods_id = goods_result[goods_index + 9: goods_index + 35].replace("'", '').split(' ')[0]
        goods_arr.append({'number': number, 'sit_time': sit_time, 'goods_id': goods_id})
    goods_list = []
    for goods in goods_arr:
        goods_str = '场地号{}，时间段：{}，商品号：{}'.format(goods['number'], goods['sit_time'], goods['goods_id'])
        goods_list.append(goods_str)

    if task_is_run is False:
        task_is_run = True
        print('\n'.join(goods_list))
        write_txt(goods_list)
    goods_info = combination(goods_arr)
    if goods_info is None:
        print('当日没有可预定场地：{0}'.format(sit_times))
        return
    token_index = goods_result.find('token')
    token = goods_result[token_index - 48:token_index - 8]
    temp_url = confirm_url.format(goods_info['goods_str'], goods_info['goods_ids'], get_total_milliseconds(init_date),
                                  token)
    confirm_start = time.perf_counter()
    confirm_response = req.get(temp_url, proxies=proxies, verify=verify_str)
    end = time.perf_counter()
    print('confirm耗时：{:.4f}s'.format(end - confirm_start))
    confirm_result = str(confirm_response.content, encoding='utf-8')
    hash_index = confirm_result.find('J_payHash')
    hash_str = confirm_result[(hash_index - 7 - 32):(hash_index - 7)]
    token_do_index = confirm_result.find('token')
    token_do_str = confirm_result[token_do_index - 47:token_do_index - 7]
    temp_url = confirm_do_url.format(goods_info['goods_ids'], hash_str, get_total_milliseconds(init_date), token_do_str)
    confirm_start = time.perf_counter()
    confirm_do_response = req.get(temp_url, proxies=proxies, verify=verify_str)
    end = time.perf_counter()
    print('confirm_do耗时：{:.4f}s'.format(end - confirm_start))
    confirm_dojson = json.loads(confirm_do_response.content)
    end = time.perf_counter()
    print('一共耗时：{:.4f}s'.format(end - start))
    print(confirm_dojson['msg'] + ',场地：' + goods_info['sit_str'])
    requests.get(notice_url.format('场地预定成功', '场地：' + goods_info['sit_str']), proxies=proxies,
                 verify=verify_str)


def schedule_task(exec_time):
    # 每天exec_time执行
    temp_time = datetime.datetime.strptime(exec_time, '%H:%M')
    schedule.every().day.at(exec_time).do(client_task)
    global task_is_run
    while True:
        if task_is_run:
            task_is_run = False
            login()
            print("下次运行时间：{}".format(schedule.next_run()))
        schedule.run_pending()
        interval = 5
        if temp_time.hour < datetime.datetime.now().hour or (
                temp_time.hour == datetime.datetime.now().hour and temp_time.minute < datetime.datetime.now().minute):
            curr_date = datetime.datetime.today() + datetime.timedelta(days=1)
        else:
            curr_date = datetime.datetime.today()
        temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
        if (temp_time - datetime.datetime.now()).total_seconds() < 30:
            interval = 0.01
        if datetime.datetime.now().hour % 6 == 5 and datetime.datetime.now().minute == 0 \
                and datetime.datetime.now().second == 0:
            login()
        time.sleep(interval)


def combination(goods_arr):
    goods_list = list(filter(lambda x: x['sit_time'] in sit_times, goods_arr))
    if len(goods_list) == 0:
        return None
    data = DataFrame(goods_list)
    time_temp_data = data.groupby('sit_time', as_index=False)['number'].count()
    if time_temp_data['number'].min() == 0:
        return None
    number_temp_data = data.groupby('number', as_index=False)['sit_time'].count()
    max_index = number_temp_data['sit_time'].argmax()
    goods_temp_list = []
    if number_temp_data['sit_time'].max() == 2:
        number = number_temp_data['number'][max_index]
        goods_temp_list = list(filter(lambda x: x['number'] == number, goods_list))
    else:

        for sit_time in sit_times:
            temp = data[data['sit_time'] == sit_time][0:1]
            if temp.size == 0:
                continue
            temp_list = list(
                filter(lambda x: x['goods_id'] == temp.iloc[0, 2],
                       goods_list))
            for temp in temp_list:
                if len([x for x in goods_temp_list if x['sit_time'] == temp['sit_time']]) == 0:
                    goods_temp_list.append(temp)
    goods_str = ''
    goods_ids = ''
    sit_str = ''
    for goods in goods_temp_list:
        price = get_price(goods['sit_time'], init_date)
        temp_str = url_param.format(price, goods['sit_time'], goods['number'], goods['sit_time'],
                                    int(goods['sit_time']) + 1)
        if goods_str == '':
            goods_str = temp_str
        else:
            goods_str = goods_str + '&' + temp_str
        if goods_ids == '':
            goods_ids = goods['goods_id']
            sit_str = goods['sit_time'] + goods['number']
        else:
            goods_ids = goods_ids + '%2C' + goods['goods_id']
            sit_str = sit_str + ',' + goods['sit_time'] + goods['number']

    return {'goods_str': goods_str, 'goods_ids': goods_ids, 'sit_str': sit_str}


def get_price(sit_time, current_date):
    if current_date.isoweekday() == 6 or current_date.isoweekday() == 7:
        return 80
    if 7 <= int(sit_time) < 10:
        return 40
    if 10 <= int(sit_time) < 15:
        return 60
    return 80


def login():
    global req
    req = requests.session()
    req.keep_alive = False
    # 登录
    data = {'username': username, 'password': password}
    login_response = req.post(login_url, data=data, proxies=proxies, verify=verify_str)

    login_json = json.loads(login_response.content)
    if login_json['code'] == '1':
        return req
    return None


def get_goods_result():
    total_seconds = get_total_milliseconds(init_date)
    goodsId_response = req.get(goods_id_url.format(total_seconds), proxies=proxies, verify=verify_str)
    return str(goodsId_response.content, encoding='utf-8')


def get_total_milliseconds(exec_date):
    current = exec_date - datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m-%d %H:%M')
    return int(current.total_seconds())


def write_txt(log):
    curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    log_date = datetime.datetime.today() + datetime.timedelta(days=pickup_days)
    with open(curr_date_str + 'log.txt', 'w', encoding='utf8') as w:
        w.write('日期{}\n'.format(log_date))
        w.write("\n".join(log))
        w.close()


if __name__ == '__main__':
    try:
        _main_()
    except Exception:
        traceback.print_exc()
    input('按任意键退出')
    sys.exit()
