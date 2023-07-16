import datetime
import json
import math
import os
import random
import sys
import threading
import time
import traceback

import psutil
import pyautogui
import schedule
import win32gui
import win32con

import requests

from comm import autoUtil

proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
verify_str = "FiddlerRoot.pem"
token_file_path = r'D:\private\51yundong.txt'
fllow_file_path = r'D:\private\yundong_info.txt'
court_url = 'https://mapv2.51yundong.me/api/stadium/resources/2c93809e821eb0ed018229e727b900af/matrix?stadiumItemId={}&date={}'
submit_url = 'https://mapv2.51yundong.me/api/order/orders?orderType=1'
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'
stadiumItemId = '2c93809e821eb0ed018229e727b900af'
stadiumId = '2c93809e821eb0ed018229e727b600ae'
headers = {
    "Content-Type": "application/json"
}
court_all_list = []
req = requests.session()
info_list = []
task_is_run = True
start = 0
logged = False
fiddler_is_start = False
start_diff = '1'
next_run_time = datetime.datetime.now()
court_sort_no = 0


def _main_():
    global info_list, start_diff, court_sort_no
    exec_time = '00:00'
    with open("configInfo/51yundong.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    if len(configList) != 4:
        print('配置文件错误！')
        input('输入任意键退出')
        sys.exit()
    for config in configList:
        config = config.replace('\uFEFF', '')
        if config.startswith('抢票时间'):
            exec_time = config.replace('\n', '').split('=')[1]
        if config.startswith('场地号'):
            field_no = config.replace('\n', '').split('=')[1]
            court_sort_no = int(field_no)
        if config.startswith('时间段'):
            times_str = config.replace('\n', '').split('=')[1]
            if times_str != '':
                times = times_str.split(',')
        if config.startswith('启动时差'):
            start_diff = config.replace('\n', '').split('=')[1]
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')

    for time_s in times:
        info_list.append({'resourceDate': init_date, 'fieldNo': 0, 'time': float(time_s), 'price': 80})
    # info_list = [{'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[0])},
    #              {'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[1])}]
    # fiddler_start()
    close_win_class()
    login()
    task(1)
    # schedule_task(exec_time)


def close_win_class():
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_0", "来沪动丨健身地图")  # 获取窗口
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    time.sleep(0.1)


def before_calc(content):
    global court_all_list, info_list
    court_all_list = calc_result_json(content)
    court_no_first = 0
    court_no_second = 0
    num = court_sort_no
    temp_first = 0
    temp_second = 0

    for item in court_all_list:
        if item['fieldNo'] == 1 or item['fieldNo'] == 9:
            continue
        if num == 0:
            break
        if int(info_list[0]['time']) == int(item['time']):
            court_no_first = item['fieldNo']
        if len(info_list) == 2 and int(info_list[1]['time']) == int(item['time']):
            court_no_second = item['fieldNo']
        if court_no_first == court_no_second and court_no_first != 0:
            temp_first = court_no_first
            temp_second = court_no_second
            court_no_first = 0
            court_no_second = 0
            num = num - 1
    if len(info_list) == 2 and (court_no_first == 0 or court_no_second == 0) and (
            temp_first == 0 or temp_second == 0):
        print('{}没有{}时间段场地'.format(info_list[0]['resourceDate'],
                                          str(int(info_list[0]['time'])) + '、' + str(
                                              int(info_list[1]['time']))))

    else:
        if len(info_list) == 1 and court_no_first == 0 and temp_first == 0:
            print('{}没有{}时间段场地'.format(info_list[0]['resourceDate'],
                                              str(int(info_list[0]['time']))))
            return False
        if len(info_list) == 2 and (court_no_first == 0 or court_no_second == 0):
            court_no_first = temp_first
            court_no_second = temp_second
        info_list[0]['fieldNo'] = court_no_first
        if len(info_list) == 2:
            info_list[1]['fieldNo'] = court_no_second


def task(days):
    global task_is_run
    task_is_run = True
    current_random = float(random.randint(float(start_diff) * 1000, (float(start_diff) + 0.5) * 1000)) / 1000
    # print('延迟{}秒'.format(current_random))
    # time.sleep(current_random)
    time.sleep(current_random)
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=days), '%Y-%m-%d')
    for info in info_list:
        info['resourceDate'] = init_date
    # info_list[0]['resourceDate'] = init_date
    # info_list[1]['resourceDate'] = init_date
    while True:
        try:

            # thread = threading.Thread(target=before_calc)
            # thread.start()
            # pickup_court()
            if os.path.exists(fllow_file_path):
                os.remove(fllow_file_path)
            auto_pickup()
            break
        except:
            traceback.print_exc()
            sys.exit()


# try:
#     if get_court():
#         pickup_court()
#         break
#     else:
#         current_random = random.randint(1000, 7000)
#         time.sleep(float(current_random)/1000)
#         print('等待{}毫秒，继续查询'.format(float(current_random)/1000))
# except:
#     traceback.print_exc()


def pickup_court():
    global start
    start = time.perf_counter()

    date_arr = info_list[0]['resourceDate'].split('-')
    stadiumSource = date_arr[0] + date_arr[1] + date_arr[2].replace('0', '')
    submit_param = {"app": "MAP", "stadiumItemId": stadiumItemId,
                    "stadiumId": stadiumId,
                    "details": [],
                    "stadiumSource": stadiumSource, "channel": 1, "orderType": "1", "userMobile": 18001716508,
                    "timestamp": int(datetime.datetime.now().timestamp() * 1000)}

    result_response = req.post(submit_url, json=submit_param, headers=headers,
                               verify=verify_str, proxies=proxies)
    result_json = json.loads(result_response.content)
    print(result_json)
    if result_json['code'] == 200:
        requests.get(notice_url.format('卢湾{}场地预订成功'.format(info_list[0]['fieldNo']), info_list))
    else:
        print('卢湾{}场地预订失败'.format(info_list[0]['fieldNo']))
        print(submit_param)
    end = time.perf_counter()
    print('提交耗时：{:.4f}s'.format(end - start))
    print('下订单成功总耗时：{:.4f}s'.format(end - start))
    print('当前时间：{}'.format(datetime.datetime.now()))


def get_court():
    global start
    start = time.perf_counter()
    temp_url = court_url.format(stadiumItemId, info_list[0]['resourceDate'])
    result_response = req.get(temp_url, headers=headers, verify=verify_str, proxies=proxies)
    end = time.perf_counter()
    print('加载场地数据耗时：{:.4f}s'.format(end - start))
    return calc_result_json(result_response.content)


def calc_result_json(content):
    result_json = json.loads(content)
    data_list = []
    for item in result_json['data']:
        for client_item in item['fieldResource']:
            if client_item['status'] == 'FREE':  # and int(client_item['start']) >= 1080:
                param = {'fieldId': item['fieldId'], 'fieldName': item['fieldName'],
                         'fieldNo': get_court_no(item['fieldName']), 'periodDate': item['periodDate'],
                         'start': client_item['start'], 'time': int(client_item['start']) / 60,
                         'price': client_item['price']}
                data_list.append(param)
    if len(data_list) == 0:
        print('{}没有场地了'.format(info_list[0]['resourceDate']))
    else:
        for item in data_list:
            print(item)
        write_txt(data_list, 'luwan.txt')
    print('3当前时间：{}'.format(datetime.datetime.now()))
    return data_list

def write_txt(log, name):
    curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(curr_date_str + '_' + name, 'w', encoding='utf8') as w:
        for item in log:
            w.write(str(item) + '\n')
        w.close()


def save_log(token):
    curr_date_str = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('access_token.txt', 'a', encoding='utf8') as w:
        w.write(curr_date_str + ' ' + token + '\n')
        w.close()


def get_court_no(court_name):
    if court_name == '一号场（单）':
        return 1
    elif court_name == '二号场':
        return 2
    elif court_name == '三号场':
        return 3
    elif court_name == '四号场':
        return 4
    elif court_name == '五号场':
        return 5
    elif court_name == '六号场':
        return 6
    elif court_name == '七号场':
        return 7
    elif court_name == '八号场':
        return 8
    elif court_name == '九号场（单）':
        return 9
    elif court_name == '十号场':
        return 10
    elif court_name == '十一号场':
        return 11
    elif court_name == '十二号场':
        return 12


def get_access_token():
    num = 0
    while True:
        if num > 1000:
            break
        if os.path.exists(token_file_path):
            print('4当前时间：{}'.format(datetime.datetime.now()))
            # if next_run_time > datetime.datetime.now():
            #     return None
            break
        time.sleep(0.01)
        num = num + 1
    try:
        with open(token_file_path, "r", encoding='UTF-16 LE') as f:
            result = f.readline().replace('\uFEFF', '').replace('\n', '')
            save_log(result)
            f.close()
        return result
    except FileNotFoundError:
        return None


def login():
    global start, logged
    logged = True
    start = time.perf_counter()
    for i in range(5):
        if os.path.exists(token_file_path):
            os.remove(token_file_path)

        os.startfile(r"C:\Users\Administrator\Desktop\来沪动丨健身地图.lnk")
        print('1当前时间：{}'.format(datetime.datetime.now()))
        access_token = get_access_token()
        print('2当前时间：{}'.format(datetime.datetime.now()))
        if access_token is None:
            print('access_token is none')
            close_win_class()
            continue
        else:
            break
    headers['Authorization'] = 'Bearer ' + access_token
    end = time.perf_counter()
    print('打开小程序耗时：{:.4f}s'.format(end - start))


def schedule_task(exec_time):
    # 每天exec_time执行
    temp_time = datetime.datetime.strptime(exec_time, '%H:%M')
    schedule.every().day.at(exec_time).do(task)
    global task_is_run, logged, fiddler_is_start, next_run_time
    while True:
        if task_is_run:
            task_is_run = False
            logged = False
            fiddler_is_start = False
            close_win_class()
            next_run_time = schedule.next_run()
            print("下次运行时间：{}".format(next_run_time))

        schedule.run_pending()
        interval = 5
        if temp_time.hour < datetime.datetime.now().hour or (
                temp_time.hour == datetime.datetime.now().hour and temp_time.minute < datetime.datetime.now().minute):
            curr_date = datetime.datetime.today() + datetime.timedelta(days=1)
        else:
            curr_date = datetime.datetime.today()
        temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
        diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
        if 600 > diff_seconds > 0 and fiddler_is_start is False:
            fiddler_start()
            time.sleep(10)
            login()
        if 0 < diff_seconds < 30:
            interval = 0.01
        # if 300> diff_seconds > 0 and logged is False:
        #     login()
        time.sleep(interval)


def fiddler_start():
    global fiddler_is_start
    fiddler_is_start = True
    close_win('Fiddler.exe')
    time.sleep(1)
    os.startfile(r"D:\private\Fiddler\Fiddler.exe")
    print('重启fiddler：{}'.format(datetime.datetime.now()))


def close_win(win_name):
    # 获取进程列表
    processes = psutil.process_iter()

    # 遍历进程列表
    for proc in processes:
        try:
            # 获取进程的名称
            process_name = proc.name()

            # 如果进程的名称是要杀死的进程的名称，则杀死该进程
            if process_name == win_name:
                proc.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(0.5)


def close_win(win_name):
    # 获取进程列表
    processes = psutil.process_iter()

    # 遍历进程列表
    for proc in processes:
        try:
            # 获取进程的名称
            process_name = proc.name()

            # 如果进程的名称是要杀死的进程的名称，则杀死该进程
            if process_name == win_name:
                proc.kill()

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    time.sleep(0.5)


def auto_pickup():
    auto_start = time.perf_counter()
    curr = autoUtil.active_window("Chrome_WidgetWin_0", "来沪动丨健身地图")
    time.sleep(0.01)
    pyautogui.click((curr[0] + 370, curr[1] + 750), clicks=1)
    time.sleep(0.2)
    pyautogui.click((curr[0] + 70, curr[1] + 350), clicks=1)
    is_run(is_success, 50, 'api/stadium/favorites')
    time.sleep(0.2)
    pyautogui.click((curr[0] + 80, curr[1] + 100), clicks=1)
    is_run(is_success, 50, 'api/stadium/resources')
    pyautogui.scroll(-900)
    time.sleep(0.2)
    load_start = time.perf_counter()
    pyautogui.click((curr[0] + 350, curr[1] + 685), clicks=1)
    is_run(is_success, 50, 'matrix?stadiumItemId')
    # 加载数据
    logs = load_log()
    for log in logs:
        infos = log.split('||')
        if len(infos) == 2 and 'matrix?stadiumItemId' in str(infos[0]):
            before_calc(infos[1])
    end = time.perf_counter()
    print('加载场地耗时：{:.4f}s'.format(end - load_start))
    pyautogui.scroll(-900)
    time.sleep(0.2)
    pyautogui.moveTo((curr[0] + 250, curr[1] + 525), duration=0)
    pyautogui.keyDown('shift')
    pyautogui.scroll(-900)
    pyautogui.keyUp('shift')
    end = time.perf_counter()
    print('选择场地前耗时：{:.4f}s'.format(end - auto_start))
    court_sum = 0
    for info in info_list:
        court_sum = court_sum + int(info['fieldNo'])
    if court_sum == 0:
        print('无场地')
        return
    x_diff = 66
    y_diff = 53
    for info in info_list:
        time.sleep(0.1)
        pyautogui.click(
            (curr[0] + 115 + x_diff * (int(info['time']) - 18)), curr[1] + 55 + y_diff * (int(info['fieldNo']) - 2),
            clicks=1)
    time.sleep(0.1)
    pyautogui.click((curr[0] + 270, curr[1] + 720), clicks=1)
    submit_result = is_run(is_success, 50, 'orders?orderType=1')
    if submit_result:
        print('提交成功')
    end = time.perf_counter()
    print('提交耗时：{:.4f}s'.format(end - auto_start))
    # time.sleep(0.5)
    # for i in range(4):
    #     for j in range(11):
    #         time.sleep(0.5)
    #         pyautogui.click((curr[0] + 115 + (i * x_diff), curr[1] + 55 + j * y_diff), clicks=1)
    # pyautogui.click((curr[0] + 147+66, curr[1] + 80), clicks=1)

    # time.sleep(0.5)
    # pyautogui.click((curr[0] + 147 + 66, curr[1] + 80+54), clicks=1)
    # pyautogui.click((curr[0] + 120+x_diff, curr[1] + 60+x_diff), clicks=1)


def is_run(task, max_num=5, args=None):
    index = 0
    while index < max_num:
        index = index + 1
        print('方法名：{}，参数：{}，run次数：{}'.format(task.__name__, args, str(index)))
        if task(args):
            return True
        else:
            time.sleep(0.1)
    return False


def is_success(args):
    logs = load_log()
    for log in logs:
        infos = log.split('||')
        if len(infos) == 2 and args in str(infos[0]):
            result = json.loads(infos[1])
            return result['code'] == 200
    return False


def load_log():
    try:
        with open(fllow_file_path, "r", encoding='UTF-16 LE') as f:
            urls = f.readlines()
            f.close()
        return urls
    except FileNotFoundError:
        return ''


if __name__ == '__main__':
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
