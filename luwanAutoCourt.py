import base64
import datetime
import json
import os
import sys
import time
import traceback

import psutil
import pyautogui
import requests
import schedule
import win32con
import win32gui

from comm import autoUtil
from ddddocr import DdddOcr

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
success_num = 0
curr_point = []
days = 6
coord6 = {}
slide_png_path = r'd:\\private\\slide.png'
bg_png_path = r'd:\\private\\bg.png'


def _main_():
    global info_list, start_diff, court_sort_no, days
    exec_times = ['00:00', '12:00']
    with open("configInfo/51yundong.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    if len(configList) != 5:
        print('配置文件错误！')
        input('输入任意键退出')
        sys.exit()
    for config in configList:
        config = config.replace('\uFEFF', '')
        if config.startswith('抢票时间'):
            exec_times = config.replace('\n', '').split('=')[1].split(',')
        if config.startswith('场地号'):
            field_no = config.replace('\n', '').split('=')[1]
            court_sort_no = int(field_no)
        if config.startswith('时间段'):
            times_str = config.replace('\n', '').split('=')[1]
            if times_str != '':
                times = times_str.split(',')
        if config.startswith('启动时差'):
            start_diff = config.replace('\n', '').split('=')[1]
        if config.startswith('抢几天后的场地'):
            days = config.replace('\n', '').split('=')[1]
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')

    for time_s in times:
        info_list.append({'resourceDate': init_date, 'fieldNo': 0, 'time': float(time_s), 'price': 80})
    # info_list = [{'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[0])},
    #              {'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[1])}]
    # fiddler_start()
    # time.sleep(2)
    # pyautogui.hotkey('winleft', 'm')
    # for i in range(1):
    #     close_win_class()
    #     login()
    #     task(2)
    schedule_task(exec_times)


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
        if court_type == 1 and (item['fieldNo'] == 1 or item['fieldNo'] == 9):
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


court_type = 2


def task(courttype):
    global task_is_run, court_type
    task_is_run = True
    court_type = courttype
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')
    for info in info_list:
        info['resourceDate'] = init_date

    while True:
        try:
            pyautogui.moveTo((curr_point[0] + 80, curr_point[1] + 100))
            if os.path.exists(fllow_file_path):
                os.remove(fllow_file_path)
            if os.path.exists(bg_png_path):
                os.remove(bg_png_path)
            if os.path.exists(slide_png_path):
                os.remove(slide_png_path)
            if court_type == 1:
                # 卢湾
                auto_pickup()
            else:
                # 万体
                wanti_auto_pickup()
            break
        except:
            traceback.print_exc()
            sys.exit()


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
    if court_type == 1:
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
    else:
        if court_name == '羽毛球3号场':
            return 1
        elif court_name == '羽毛球4号场':
            return 2
        elif court_name == '羽毛球5号场':
            return 3
        elif court_name == '羽毛球6号场':
            return 4
        elif court_name == '羽毛球7号场':
            return 5
        elif court_name == '羽毛球8号场':
            return 6


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
    global start, logged, curr_point, coord6
    logged = True
    start = time.perf_counter()

    for i in range(5):
        if os.path.exists(token_file_path):
            os.remove(token_file_path)
        os.startfile(r"C:\Users\Administrator\Desktop\来沪动丨健身地图.lnk")
        print('1当前时间：{}'.format(datetime.datetime.now()))
        # access_token = get_access_token()
        time.sleep(2)
        is_run(is_success, 100, '/api/user/users/info')
        print('2当前时间：{}'.format(datetime.datetime.now()))
        # if access_token is None:
        #     print('access_token is none')
        #     close_win_class()
        #
        #     continue
        # else:
        #     break
    try:
        curr_point = autoUtil.active_window("Chrome_WidgetWin_0", "来沪动丨健身地图")
    except:
        print('未获得焦点')
        traceback.print_exc()
    print(curr_point)
    # 6 滑块
    coord6 = (curr_point[0] + 95, curr_point[1] + 525)
    time.sleep(0.5)
    pyautogui.click((curr_point[0] + 370, curr_point[1] + 750), clicks=1, duration=1)
    time.sleep(0.5)
    pyautogui.click((curr_point[0] + 70, curr_point[1] + 350), clicks=1, duration=1)
    is_run(is_success, 100, 'api/stadium/favorites')
    # headers['Authorization'] = 'Bearer ' + access_token
    end = time.perf_counter()
    print('打开小程序耗时：{:.4f}s'.format(end - start))


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
    global success_num
    auto_start = time.perf_counter()
    print('开始：{}'.format(datetime.datetime.now()))
    pyautogui.click((curr_point[0] + 80, curr_point[1] + 100), clicks=1, duration=0.1)
    is_run(is_success, 100, 'api/stadium/resources')
    # 检查加载了几个日期的场地
    print('开始检查：{}'.format(datetime.datetime.now()))
    is_scroll = False
    click_y = 685
    logs = load_log()
    for log in logs:
        infos = log.split('||')
        if len(infos) == 2 and 'api/stadium/resources' in str(infos[0]):
            json_result = json.loads(infos[1])
            is_scroll = len(json_result['data']) == 2
    time.sleep(0.1)
    if is_scroll:
        pyautogui.scroll(-100)
        time.sleep(0.2)
    else:
        click_y = 710
    print('场馆详情页面点击：{}'.format(datetime.datetime.now()))
    pyautogui.click((curr_point[0] + 350, curr_point[1] + click_y), clicks=1, duration=0)
    print('场馆详情页面点击后：{}'.format(datetime.datetime.now()))
    is_run(is_success, 100, 'matrix?stadiumItemId')
    print('开始加载数据：{}'.format(datetime.datetime.now()))
    load_start = time.perf_counter()
    # 加载数据
    logs = load_log()
    for log in logs:
        infos = log.split('||')
        if len(infos) == 2 and 'matrix?stadiumItemId' in str(infos[0]):
            before_calc(infos[1])
    end = time.perf_counter()
    print('加载场地耗时：{:.4f}s'.format(end - load_start))
    print('加载完毕：{}'.format(datetime.datetime.now()))

    pyautogui.moveTo((curr_point[0] + 250, curr_point[1] + 525), duration=0)
    time.sleep(0.1)
    pyautogui.scroll(-900)
    time.sleep(0.1)
    num = int(info_list[0]['time'])
    if num > 18:
        num = 18
    pyautogui.keyDown('shift')
    pyautogui.scroll(-24 * (num - 9))
    pyautogui.keyUp('shift')
    end = time.perf_counter()
    print('选择场地前耗时：{:.4f}s'.format(end - auto_start))
    print('开始选择场地：{}'.format(datetime.datetime.now()))
    court_sum = 0
    for info in info_list:
        court_sum = court_sum + int(info['fieldNo'])
    if court_sum == 0:
        print('无场地')
        return
    x_diff = 66
    y_diff = 53
    variate = 2
    for info in info_list:
        time.sleep(0.1)
        pyautogui.click(
            (curr_point[0] + 115 + x_diff * (int(info['time']) - num)),
            curr_point[1] + 55 + y_diff * (int(info['fieldNo']) - variate),
            clicks=1)
        if int(info['fieldNo']) > 10:
            pyautogui.moveTo((curr_point[0] + 250, curr_point[1] + 325), duration=0)
            time.sleep(0.1)
            variate = 5
            pyautogui.scroll(-55)
            time.sleep(0.1)

    time.sleep(0.1)
    # success_num = success_num + 1
    # end = time.perf_counter()
    # print('成功耗时：{:.4f}s'.format(end - auto_start))
    # return
    pyautogui.click((curr_point[0] + 270, curr_point[1] + 720), clicks=1, duration=0.2)
    for i in range(5):
        code_validation()
        submit_result = is_run(is_success, 50, 'orders?orderType=1')
        if submit_result:
            break
        else:
            time.sleep(0.5)

    info_str = str(info_list[0]['time'])
    if submit_result:

        if len(info_list) == 2:
            info_str = str(info_list[0]['time']) + '、' + str(info_list[1]['time'])
        print('卢湾{}场地预订成功,时间点：{}'.format(info_list[0]['fieldNo'], info_str))
        # requests.get(notice_url.format('卢湾{}场地预订成功'.format(info_list[0]['fieldNo']), info_list))
    else:
        print('卢湾{}场地预订失败,时间点：{}'.format(info_list[0]['fieldNo'], info_str))
    end = time.perf_counter()
    print('提交耗时：{:.4f}s'.format(end - auto_start))


def is_run(task, max_num=5, args=None):
    index = 0
    while index < max_num:
        index = index + 1
        print('方法名：{}，参数：{}，run次数：{}，时间：{}'.format(task.__name__, args, str(index), datetime.datetime.now()))
        if task(args):
            return True
        else:
            time.sleep(0.1)
    return False


def is_success(args):
    logs = load_log()
    for i in range(len(logs) - 1, -1, -1):
        infos = logs[i].split('||')
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


def wanti_auto_pickup():
    global success_num, info_list
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=int(days)), '%Y-%m-%d')
    for info in info_list:
        info['resourceDate'] = init_date
    auto_start = time.perf_counter()
    print('万体抢场地开始：{}'.format(datetime.datetime.now()))
    pyautogui.click((curr_point[0] + 280, curr_point[1] + 100), clicks=1, duration=0.1)
    is_run(is_success, 200, 'api/stadium/resources')

    # 点击展开
    pyautogui.click((curr_point[0] + 367, curr_point[1] + 512), clicks=1, duration=0.3)
    time.sleep(0.2)
    # 点击羽毛球空间
    pyautogui.click((curr_point[0] + 150, curr_point[1] + 555), clicks=1, duration=0.1)
    is_run(is_success, 200, 'dates?stadiumItemId')
    time.sleep(0.2)
    # 往下滚动
    pyautogui.scroll(-500)
    time.sleep(0.2)
    # 点击最新日期
    print('场馆详情页面点击：{}'.format(datetime.datetime.now()))
    pyautogui.click((curr_point[0] + 345, curr_point[1] + (int(days) * 57) + 300), clicks=1, duration=0.1)
    print('开始加载数据：{}'.format(datetime.datetime.now()))
    load_start = time.perf_counter()
    is_run(is_success, 200, 'matrix?stadiumItemId')

    # 加载数据
    logs = load_log()
    for log in logs:
        infos = log.split('||')
        if len(infos) == 2 and 'matrix?stadiumItemId' in str(infos[0]):
            before_calc(infos[1])
    end = time.perf_counter()
    print('加载场地耗时：{:.4f}s'.format(end - load_start))
    print('加载完毕：{}'.format(datetime.datetime.now()))

    pyautogui.moveTo((curr_point[0] + 250, curr_point[1] + 355), duration=0)
    time.sleep(0.1)
    pyautogui.scroll(-100)
    time.sleep(0.1)
    num = int(info_list[0]['time'])
    if num > 18:
        num = 18
    pyautogui.keyDown('shift')
    pyautogui.scroll(-25 * (num - 8))
    pyautogui.keyUp('shift')
    end = time.perf_counter()
    print('选择场地前耗时：{:.4f}s'.format(end - auto_start))
    print('开始选择场地：{}'.format(datetime.datetime.now()))
    court_sum = 0
    for info in info_list:
        court_sum = court_sum + int(info['fieldNo'])
    if court_sum == 0:
        print('无场地')
        return
    x_diff = 66
    y_diff = 53
    variate = 2
    for info in info_list:
        time.sleep(0.1)
        pyautogui.click((curr_point[0] + 135 + x_diff * (int(info['time']) - num)),
                        (curr_point[1] + 150 + y_diff * (int(info['fieldNo'])) - variate), clicks=1)
        if int(info['fieldNo']) > 10:
            pyautogui.moveTo((curr_point[0] + 250, curr_point[1] + 325), duration=0)
            time.sleep(0.1)
            variate = 5
            pyautogui.scroll(-55)
            time.sleep(0.1)

    time.sleep(0.1)

    pyautogui.click((curr_point[0] + 270, curr_point[1] + 720), clicks=1, duration=0.2)
    for i in range(5):
        code_validation()
        submit_result = is_run(is_success, 50, 'orders?orderType=1')
        if submit_result:
            break
        else:
            time.sleep(0.5)
    # submit_result = is_run(is_success, 50, 'orders?orderType=1')
    info_str = str(info_list[0]['time'])
    court_no = str(int(info_list[0]['fieldNo']) + 2)
    if submit_result:

        if len(info_list) == 2:
            info_str = str(info_list[0]['time']) + '、' + str(info_list[1]['time'])
        print('万体{}场地预订成功,时间点：{}'.format(court_no, info_str))
        # requests.get(notice_url.format('卢湾{}场地预订成功'.format(info_list[0]['fieldNo']), info_list))
    else:
        print('万体{}场地预订失败,时间点：{}'.format(court_no, info_str))
    end = time.perf_counter()
    print('提交耗时：{:.4f}s'.format(end - auto_start))


def schedule_task(exec_times):
    # 每天exec_time执行
    temp_times = []
    for info in exec_times:
        temp_times.append(datetime.datetime.strptime(info, '%H:%M:%S'))
    schedule.every().day.at(exec_times[0]).do(task, 1)
    schedule.every().day.at(exec_times[1]).do(task, 2)
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
        for temp_time in temp_times:
            if temp_time.hour < datetime.datetime.now().hour or (
                    temp_time.hour == datetime.datetime.now().hour and temp_time.minute < datetime.datetime.now().minute):
                curr_date = datetime.datetime.today() + datetime.timedelta(days=1)
            else:
                curr_date = datetime.datetime.today()
            temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour,
                                          temp_time.minute)
            diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
            if 600 > diff_seconds > 0 and fiddler_is_start is False:
                fiddler_start()
                time.sleep(10)
                pyautogui.hotkey('winleft', 'm')
                time.sleep(0.5)
                login()
            if 0 < diff_seconds < 30:
                interval = 0.01

        time.sleep(interval)


def code_validation():
    for i in range(50):
        if os.path.exists(slide_png_path) is False:
            time.sleep(0.2)
        else:
            break
    if os.path.exists(slide_png_path) is False:
        print('10秒未弹出滑动框')
        return
    det = DdddOcr(det=False, ocr=False)
    target_bytes = read_img(slide_png_path)

    background_bytes = read_img(bg_png_path)
    diff = 0
    res = det.slide_match(target_bytes, background_bytes, simple_target=True)
    pyautogui.moveTo(coord6, duration=0)
    time.sleep(0.5)
    length = (res['target'][0]) - diff
    pyautogui.dragRel(length, 0, duration=0.5, button='left')
    print(length)


def read_img(file):
    with open(file, 'rb') as f:
        img_data = f.read()
        base64_data = base64.b64encode(img_data)
        # print(type(base64_data))
        # # print(base64_data)
        # # 如果想要在浏览器上访问base64格式图片，需要在前面加上：data:image/jpeg;base64,
        # base64_str = str(base64_data, 'utf-8')
        # print(base64_str)
        return img_data


if __name__ == '__main__':
    # curr_point = autoUtil.active_window("Chrome_WidgetWin_0", "来沪动丨健身地图")
    # coord6 = (curr_point[0] + 95, curr_point[1] + 525)
    # code_validation()
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
