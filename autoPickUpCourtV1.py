# author: yf
# date: 2022/11/05 16:12
import base64
import datetime
import json
import os
import random
import sys
import time
import traceback
from asyncio import as_completed
from concurrent.futures import as_completed
from ctypes import windll
from itertools import groupby

import numpy as np
import psutil
import pyautogui
import pyperclip
import requests
import schedule
import win32con
import win32gui
from chinese_calendar import is_holiday, is_workday

from ddddocr import DdddOcr
import pynput

temp_url = "https://user.jusssportsvenue.com/api/block/ground/list?venuesId={}&sportsType=9&startTime={}&skuId={}"
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'
group_param = [
    {'venuesId': 30, 'skuId': 35},
    {'venuesId': 30, 'skuId': 36},
    # {'venuesId': 30, 'skuId': 37},
    {'venuesId': 27, 'skuId': 38},
]
timespans = ['1830', '1900', '1930', '2000']
week_timespans = ['1300', '1330', '1400', '1430', '1500', '1530', '1600', '1630', '1700', '1730', '1800', '1830',
                  '1900', '1930', '2000']
random_start = 40
random_end = 60
wechat_list = []
wechat_name = []
names = []
proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
config = {'date': 20230213, 'time': [1300, 1400], 'sites': [34]}
log_file_path = r'D:\private\load_step.txt'
ground_file_path = r'D:\private\load_ground.txt'
answer_file_path = r'D:\private\answer.txt'
customRules_log_path = r'D:\private\customRules_log.txt'
plugin_path = r'D:\Users\Administrator\AppData\Roaming\Tencent\WeChat\XPlugin\Plugins\WMPFRuntime'
u = windll.LoadLibrary('user32.dll')
task_is_run = True
init_date = ''
field_no = 30
times = []
logged = False
pickup_days = 6
real_days = 7
court_times = []
court_field_no = 30

coord1 = {}
coord2 = {}
coord3 = {}
coord4 = {}
coord5 = {}
coord6 = {}
coord7 = {}
coord8 = {}
success = 0
error = 0
duration = 0.5
court_no = ''
db_file_path = ''
buy_account = 'test'
orderJson = [
    {'id': '159-羽毛球17号场-11', 'status': 1, 'userName': None, 'userPhone': None, 'userId': None, 'userAvatar': None,
     'groundId': 159, 'groundName': '羽毛球17号场', 'isNormal': True, 'sportsType': 9, 'price': 120, 'source': None,
     'isChoosing': False, 'isCheckout': None, 'orderId': None, 'noteType': None, 'name': '羽毛球17号场',
     'startTime': 1692270000000, 'endTime': 1692273600000, 'chosen': True},
    {'id': '159-羽毛球17号场-12', 'status': 1, 'userName': None, 'userPhone': None, 'userId': None, 'userAvatar': None,
     'groundId': 159, 'groundName': '羽毛球17号场', 'isNormal': True, 'sportsType': 9, 'price': 120, 'source': None,
     'isChoosing': False, 'isCheckout': None, 'orderId': None, 'noteType': None, 'name': '羽毛球17号场',
     'startTime': 1692273600000, 'endTime': 1692277200000, 'chosen': True}]

target_time = ''
work_price_dict = [{'court_time': '08', 'price': 50},
                   {'court_time': '09', 'price': 50},
                   {'court_time': '10', 'price': 50},
                   {'court_time': '11', 'price': 50},
                   {'court_time': '12', 'price': 100},
                   {'court_time': '13', 'price': 100},
                   {'court_time': '14', 'price': 100},
                   {'court_time': '15', 'price': 100},
                   {'court_time': '16', 'price': 100},
                   {'court_time': '17', 'price': 120},
                   {'court_time': '18', 'price': 120},
                   {'court_time': '19', 'price': 120},
                   {'court_time': '20', 'price': 120},
                   {'court_time': '21', 'price': 120},
                   {'court_time': '22', 'price': 120}]

weekend_price_list = [{'court_time': '08', 'price': 50},
                      {'court_time': '09', 'price': 120},
                      {'court_time': '10', 'price': 120},
                      {'court_time': '11', 'price': 120},
                      {'court_time': '12', 'price': 120},
                      {'court_time': '13', 'price': 120},
                      {'court_time': '14', 'price': 120},
                      {'court_time': '15', 'price': 120},
                      {'court_time': '16', 'price': 120},
                      {'court_time': '17', 'price': 120},
                      {'court_time': '18', 'price': 120},
                      {'court_time': '19', 'price': 120},
                      {'court_time': '20', 'price': 120},
                      {'court_time': '21', 'price': 120},
                      {'court_time': '22', 'price': 120}]
start_interval = 1


def _main_():
    global court_field_no, court_times, real_days, success, error, db_file_path, buy_account, start_interval
    if not os.path.exists('D:\\private'):
        os.makedirs('D:\\private')
    with open("autojiushi.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    if len(configList) != 7:
        print('配置文件错误！')
        input('输入任意键退出')
        sys.exit()
    for config_str in configList:
        if config_str.startswith('抢票时间'):
            exec_time = config_str.replace('\n', '').split('=')[1]
        if config_str.startswith('场地号'):
            court_field_no = config_str.replace('\n', '').split('=')[1]
        if config_str.startswith('时间段'):
            times_str = config_str.replace('\n', '').split('=')[1]
            if times_str != '':
                court_times = times_str.split(',')
        if config_str.startswith('几天后'):
            real_days = config_str.replace('\n', '').split('=')[1]
        if config_str.startswith('当前账号'):
            buy_account = config_str.replace('\n', '').split('=')[1]
        if config_str.startswith('数据库路径'):
            db_file_path = config_str.replace('\n', '').split('=')[1]
        if config_str.startswith('启动间隔'):
            start_interval = config_str.replace('\n', '').split('=')[1]
    # pickup_days = 7
    # field_no = '8'
    # times = ['15', '16']
    # for i in range(1):
    #     prepare()
    #     if pickup_court():
    #         break
    # exec_time = '23:50'
    # active_window()
    # update_body_txt()
    # pickup_new(exec_time)
    # last_pickup()

    schedule_task(exec_time)


def update_body_txt():
    global target_time
    group_id = ''
    court_number = int(court_field_no)
    if court_number == 1 or court_number == 2:
        group_id = court_number + 175
        for i in range(len(court_times)):
            court_times[i] = court_times[i] + '30'
    if 9 > court_number > 2:
        group_id = court_number + 177 - 2
        for i in range(len(court_times)):
            court_times[i] = court_times[i] + '30'
    if 34 > court_number > 8:
        group_id = court_number + 150 - 8
        for i in range(len(court_times)):
            court_times[i] = court_times[i] + '00'
    if 36 > court_number > 33:
        group_id = court_number + 215 - 33
        for i in range(len(court_times)):
            court_times[i] = court_times[i] + '00'
    start_time = create_court_time(court_times[0])
    end_time = create_court_time(str(int(court_times[0]) + 100))
    if len(court_times) == 2:
        end_time = create_court_time(court_times[1])
        last_time = create_court_time(str(int(court_times[1]) + 100))
    orderJson[0]['startTime'] = start_time
    orderJson[0]['endTime'] = end_time
    orderJson[0]['groundId'] = group_id
    orderJson[0]['id'] = "{}-羽毛球{}号场-{}".format(str(group_id), str(court_number),
                                                     str(int(court_times[0][0:2]) - 8))
    orderJson[0]['groundName'] = "羽毛球{}号场".format(str(court_number))
    orderJson[0]['name'] = "羽毛球{}号场".format(str(court_number))
    if len(court_times) == 2:
        orderJson[1]['startTime'] = end_time
        orderJson[1]['endTime'] = last_time
        orderJson[1]['groundId'] = group_id
        orderJson[1]['id'] = "{}-羽毛球{}号场-{}".format(str(group_id), str(court_number),
                                                         str(int(court_times[1][0:2]) - 8))
        orderJson[1]['groundName'] = "羽毛球{}号场".format(str(court_number))
        orderJson[1]['name'] = "羽毛球{}号场".format(str(court_number))
    today = datetime.datetime.today()
    target_time = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=int(real_days))
    price_list = work_price_dict
    if is_holiday(target_time):
        price_list = weekend_price_list
    for price_item in price_list:
        if price_item['court_time'] == court_times[0][0:2]:
            orderJson[0]['price'] = price_item['price']
        if len(court_times) == 2:
            if price_item['court_time'] == court_times[1][0:2]:
                orderJson[1]['price'] = price_item['price']
    if len(court_times) == 1:
        orderJson.remove(orderJson[1])
    result_str = json.dumps(orderJson)
    result_str = 'orderJson=' + result_str
    result_str = result_str.encode('latin-1').decode('unicode_escape').replace(' ', '')
    with open('D:\\private\\createBlcok_body_input.txt', 'w+', encoding='UTF-16') as f:
        f.write(result_str)
        f.close()


def create_court_time(timespan):
    today = datetime.datetime.today()
    item_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=int(real_days))
    return get_total_milliseconds(item_date +
                                  datetime.timedelta(hours=int(timespan[0:2]),
                                                     minutes=int(timespan[2:4])))


def pickup_new(exec_time):
    global field_no, times, pickup_days
    update_body_txt()
    pickup_days = 6
    temp_time = datetime.datetime.strptime(exec_time, '%H:%M')
    curr_date = datetime.datetime.today()
    temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
    target_is_workday = is_workday(temp_time + datetime.timedelta(days=int(real_days)))
    for i in range(2, pickup_days):
        calc_time = temp_time + datetime.timedelta(days=i)
        if target_is_workday:
            if is_workday(calc_time):
                pickup_days = i
                break
        else:
            if is_holiday(calc_time):
                pickup_days = i
                break
    info = exec_search()

    field_no = info['site']
    times = [info['time'][0:2]]
    pickup_court()
    # with pynput.mouse.Listener(on_click=on_click) as listener:
    #     listener.join()

    while True:

        diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
        if 0 < diff_seconds < 20:
            print('12点数据收集中，等待{}秒'.format(str(diff_seconds + 0.01)))
            time.sleep(diff_seconds - float(start_interval))
            last_pickup()
        else:
            time.sleep(5)


def manual_exec(day_input, field_no_input, times_input):
    global pickup_days, field_no, times
    pickup_days = day_input
    field_no = field_no_input
    times = times_input

    pickup_court()


def schedule_task(exec_time):
    # 每天exec_time执行
    temp_time = datetime.datetime.strptime(exec_time, '%H:%M') + datetime.timedelta(minutes=-1)
    before_time_str = datetime.datetime.strftime(temp_time, '%H:%M')
    schedule.every().day.at(before_time_str).do(pickup_new, exec_time)
    global task_is_run, logged
    while True:
        if task_is_run:
            task_is_run = False
            logged = False
            print("下次运行时间：{}".format(schedule.next_run()))

        schedule.run_pending()
        interval = 5
        if temp_time.hour < datetime.datetime.now().hour or (
                temp_time.hour == datetime.datetime.now().hour and temp_time.minute < datetime.datetime.now().minute):
            curr_date = datetime.datetime.today() + datetime.timedelta(days=1)
        else:
            curr_date = datetime.datetime.today()
        temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
        diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
        if diff_seconds < 10:
            interval = 0.01
        if 600 >= diff_seconds > 0 and logged is False:
            close_win("WeChatAppEx.exe")
            prepare()
        time.sleep(interval)


def close_win(win_name):
    # hwnd = win32gui.FindWindow("Chrome_WidgetWin_0", "久事体育场馆")  # 获取窗口
    # win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
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


def login_wechat():
    close_win("WeChat.exe")
    os.startfile(r"C:\Users\Administrator\Desktop\微信.lnk")
    time.sleep(1)
    hwnd = win32gui.FindWindow("WeChatLoginWndForPC", "微信")  # 获取窗口
    if hwnd == 0:
        print('微信窗口未打开')
        return
    if win32gui.IsWindowVisible(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    if win32gui.IsIconic(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)
    curr = win32gui.GetWindowRect(hwnd)
    print(curr)
    # 1 登录
    login_coord = (curr[0] + 140, curr[1] + 280)
    pyautogui.click(login_coord, clicks=1, duration=0.5)


def prepare():
    global logged
    logged = True
    login_wechat()
    time.sleep(10)
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")  # 获取窗口
    # show_info = win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    # print(show_info)
    for i in range(2):
        close_win("WeChatAppEx.exe")
        if os.path.exists(log_file_path):
            os.remove(log_file_path)
        if os.path.exists(answer_file_path):
            os.remove(answer_file_path)
        if os.path.exists(customRules_log_path):
            os.remove(customRules_log_path)

        os.startfile(r"C:\Users\Administrator\Desktop\久事体育场馆.lnk")
        is_run(first_is_success, 200)
        win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
        time.sleep(1)
        active_window()
        if click_start():
            break


def exec_pickup():
    for i in range(1):
        if pickup_court():
            break
        close_win("WeChatAppEx.exe")
        prepare()


def pickup_court():
    global init_date, task_is_run
    start = time.perf_counter()
    print('当前时间：{}'.format(datetime.datetime.now()))
    if active_window() is False:
        return False
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=int(pickup_days)),
                                           '%Y%m%d')
    task_is_run = True
    pick_up()
    if is_run(get_price_is_success, 20) is False:
        return False


def last_pickup():
    active_window()
    start = time.perf_counter()
    print('时间{},开始预订'.format(datetime.datetime.now()))
    for i in range(20):
        code_validation()
        if get_answer(['correct answer']):
            end = time.perf_counter()
            print('验证码通过耗时：{:.4f}s'.format(end - start))
            print('当前时间：{}'.format(datetime.datetime.now()))
            if is_run(pay_is_begin, 100) is False:
                print('时间{}, 场地{},时间{}已经被预订'.format(datetime.datetime.now(), field_no, times))
                break
            pyautogui.click(coord8, clicks=1)
            print('{}，订购成功,场地{},时间{},购买账号{}'.format(datetime.datetime.now(), court_field_no, court_times,
                                                                buy_account))
            requests.get(
                notice_url.format('预定场地成功',
                                  '预定场地成功,等待付款,日期{},场地{},时间{},购买账号{}'.format(target_time,
                                                                                                 court_field_no,
                                                                                                 court_times,
                                                                                                 buy_account)),
                proxies=proxies,
                verify="FiddlerRoot.pem")
            return True
        else:
            time.sleep(0.6)
            continue
    end = time.perf_counter()
    print('3失败耗时：{:.4f}s'.format(end - start))
    return False


def active_window():
    global coord1, coord2, coord3, coord4, coord5, coord6, coord7, coord8
    result = u.GetForegroundWindow()
    if result == 0 or result == 67622:
        print('锁屏状态不能推送消息')
        return False
    # windll.user32.BlockInput(1)
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_0", "久事体育场馆")  # 获取窗口
    if hwnd == 0:
        print('久事体育窗口未打开')
        return False
    if win32gui.IsWindowVisible(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    if win32gui.IsIconic(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)
    curr = win32gui.GetWindowRect(hwnd)
    # 1 羽毛球
    coord1 = (curr[0] + 280, curr[1] + 380)
    # 2 我要订场
    coord2 = (curr[0] + 320, curr[1] + 450)
    # 3 场馆
    coord3 = (curr[0] + 32, curr[1] + 187)
    # 4 12
    coord4 = (curr[0] + 18, curr[1] + 223)
    # 5 确认提交
    coord5 = (curr[0] + 330, curr[1] + 710)
    # 6 滑块
    coord6 = (curr[0] + 95, curr[1] + 525)

    # 7 刷新
    coord7 = (curr[0] + 330, curr[1] + 557)
    # 8 立即支付
    coord8 = (curr[0] + 330, curr[1] + 710)
    return True


def get_answer(captcha_msg):
    try:
        with open(answer_file_path, "r", encoding='UTF-16 LE') as f:
            result = f.readline().replace('\uFEFF', '')
            f.close()
        for msg in captcha_msg:
            if msg in result:
                return True
    except FileNotFoundError:
        return False


def verification_is_success():
    image_l = pyautogui.locateOnScreen('img\\5.png', 5)
    return image_l is None


def pay_is_begin(args):
    url = load_log()
    if 'paymentList' in url:
        return True
    else:
        return False


def first_is_success(args):
    url = load_log()
    if '/train/api/course/hot/list' in url:
        return True
    else:
        return False


def second_is_success(args):
    url = load_log()
    if '/api/venues/getList' in url:
        return True
    else:
        return False


def third_is_success(args):
    url = load_log()
    if '/api/block/filter?storeId=4' in url:
        return True
    else:
        return False


def get_price_is_success(args):
    url = load_log()
    if '/api/block/status/priceList' in url:
        return True
    else:
        return False


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


def code_validation():
    if is_run(get_answer, 50, args=['Get the verification code information successfully', 'wrong answer']) is False:
        return
    for i in range(20):
        image_l = pyautogui.locateOnScreen('img\\05.png', grayscale=True)
        if image_l is not None:
            # image_l = pyautogui.locateOnScreen('img\\005.png', grayscale=True)
            # center = pyautogui.center(image_l)
            pyautogui.click(coord7, clicks=1)
            is_run(get_answer, 50, args=['Get the verification code information successfully', 'wrong answer'])
        else:
            break

    det = DdddOcr(det=False, ocr=False)
    with open(customRules_log_path, "r", encoding='UTF-16 LE') as f:
        imageDataL = f.readline().replace('\uFEFF', '').replace('\n', '')
        ImageDataS = f.readline().replace('\uFEFF', '').replace('\n', '')
        f.close()
    target_bytes = base64.b64decode(imageDataL)
    background_bytes = base64.b64decode(ImageDataS)
    res = det.slide_match(target_bytes, background_bytes, simple_target=True)
    pyautogui.moveTo(coord6, duration=0)
    time.sleep(0.5)
    # move_distance = valid_coord[0] - coord6[0]
    # square_x = (res['target'][2] - res['target'][0])
    length = (res['target'][0]) / 2 - random.randint(20, 22)
    print('滑动距离{}'.format(length))
    # print('手动测量滑动距离{}'.format(move_distance))
    # pyautogui.dragRel(move_distance, 0, duration=0.8, button='left')
    pyautogui.mouseDown(button='left')
    pyautogui.moveTo(length + coord6[0], coord6[1], duration=0.4)
    time.sleep(0.3)
    pyautogui.mouseUp(button='left')
    is_run(get_answer, 10, args=['correct answer'])


# 加载指定日期场地信息
def is_load_ground(load_info):
    venues_id = load_info['venues_id']
    start_time = load_info['start_time']
    sku_id = load_info['sku_id']
    if os.path.exists(ground_file_path) is False:
        return False
    with open(ground_file_path, "r", encoding='UTF-16 LE') as f:
        urls = f.readlines()
        f.close()
    for url in urls:
        if 'venuesId={}'.format(str(venues_id)) in url and 'startTime={}'.format(
                str(start_time)) in url and 'skuId={}'.format(str(sku_id)) in url:
            return True
    return False
    # index = url.find('?')
    # temp = url[index + 1:len(url)]
    # list_arr = temp.split('&')
    # return str(venues_id) == list_arr[0].replace('venuesId=', '') and list_arr[
    #     2].replace('startTime=', '') == str(start_time) and list_arr[3].replace('skuId=', '') == str(sku_id)


def load_log():
    try:
        with open(log_file_path, "r", encoding='UTF-16 LE') as f:
            urls = f.readlines()
            f.close()
        return ','.join(urls)
    except FileNotFoundError:
        return ''


def click_start():
    # image_l = find_image('img\\0.png', 20)
    # center = pyautogui.center(image_l)
    # print(center)
    pyautogui.click(coord1, clicks=1, duration=duration)
    if is_run(second_is_success, 200) is False:
        return False
    # image_l = find_image('img\\00.png', 20)
    # center = pyautogui.center(image_l)
    # print(center)
    pyautogui.click(coord2, clicks=1, duration=duration)
    if is_run(third_is_success, 200) is False:
        return False
    return True


def find_image(image, num):
    index = 0
    while index < num:
        image_l = pyautogui.locateOnScreen(image, grayscale=True)
        if image_l is None:
            time.sleep(0.1)
            index = index + 1
            continue
        else:
            return image_l
            break

    return None


def click_venue(x, y, sku_id):
    if sku_id == 38:
        pyautogui.click(x + 280, y + 40, clicks=1, duration=duration)
    else:
        pyautogui.click(x + 100, y + 40, clicks=1, duration=duration)


def click_court(x, y, sku_id):
    if sku_id == 38 or sku_id == 35:
        pyautogui.click(x + 50, y + 220, clicks=1, duration=duration)
    if sku_id == 36:
        pyautogui.click(x + 210, y + 220, clicks=1, duration=duration)
    if sku_id == 37:
        pyautogui.click(x + 330, y + 220, clicks=1, duration=duration)


def click_day(x, y, days):
    if os.path.exists(ground_file_path):
        os.remove(ground_file_path)
    pyautogui.click(x, y + 300, clicks=0, duration=duration)
    time.sleep(0.01)
    index = days
    if days > 3:
        # 按住shift，往右滚动
        pyautogui.keyDown('shift')
        pyautogui.scroll(-900)
        pyautogui.keyUp('shift')
        time.sleep(0.1)
        if datetime.datetime.now().hour >= 12:
            index = days - 4
        else:
            index = days - 3
    pyautogui.click(x + index * 100, y + 300, clicks=1, duration=duration)
    if days == 0:
        pyautogui.click(x + 100, y + 300, clicks=0, duration=duration)
    time.sleep(0.01)


def click_time(court_id, time_ids):
    # 向下滚动
    time.sleep(0.2)
    pyautogui.scroll(-200)
    time.sleep(0.2)
    # 标点19：30
    # img = 'img\\03.png'
    # image_l = find_image(img, 20)
    # center = pyautogui.center(image_l)
    x, y = coord4[0], coord4[1]
    # 按住shift，往右滚动
    if court_id > 1:
        pyautogui.moveTo(x + 40, y, duration=duration)
        pyautogui.keyDown('shift')
        if court_id >= 9:
            scroll = court_id - 9
        else:
            scroll = court_id - 3
        pyautogui.scroll(-36 * scroll)
        pyautogui.keyUp('shift')
        time.sleep(0.01)
    for time_id in time_ids:
        if court_id in [5, 6, 7, 8]:
            pyautogui.click(x + (court_id - 4) * 80, y + (int(time_id) - 12) * 40, clicks=1,
                            duration=duration)
            continue
        if court_id > 32:
            pyautogui.click(x + (court_id - 31) * 80, y + (int(time_id) - 12) * 40, clicks=1,
                            duration=duration)
            continue
        if court_id == 2:
            pyautogui.click(x + court_id * 80, y + (int(time_id) - 12) * 40, clicks=1,
                            duration=duration)
            continue
        pyautogui.click(x + 80, y + (int(time_id) - 12) * 40, clicks=1,
                        duration=duration)
        time.sleep(0.01)


def pick_up():
    court_id = int(field_no)
    item_date = datetime.datetime.strptime(init_date, '%Y%m%d')
    days = (item_date.date() - datetime.date.today()).days
    if court_id < 3:
        venuesId = group_param[0]['venuesId']
        skuId = group_param[0]['skuId']
    if 9 > court_id > 2:
        venuesId = group_param[1]['venuesId']
        skuId = group_param[1]['skuId']
    if court_id > 8:
        venuesId = group_param[2]['venuesId']
        skuId = group_param[2]['skuId']
    time.sleep(0.1)
    # image_l = find_image('img\\01.png', 20)
    # center = pyautogui.center(image_l)
    x, y = coord3[0], coord3[1]
    # 点击9-33
    click_venue(x, y, skuId)
    # 点击9-21号场
    time.sleep(0.1)
    click_court(x, y, skuId)
    # 点击days天后
    time.sleep(0.1)
    click_day(x, y, days)

    start_time = get_total_milliseconds(item_date)
    is_run(is_load_ground, 200, {'venues_id': venuesId, 'start_time': start_time, 'sku_id': skuId})

    # 点击时间场地
    click_time(court_id, times)
    # 点击确认
    # image_l = find_image('img\\4.png', 20)
    # center = pyautogui.center(image_l)
    pyautogui.click(coord5, clicks=1, duration=0)
    time.sleep(0.1)


def exec_search():
    print("{}开始搜索空闲场地~~".format(datetime.datetime.now()))
    result = []
    sku_id = 36
    if int(court_field_no) > 8:
        sku_id = 38
    for item in group_param:
        if item['skuId'] != sku_id:
            continue
        today = datetime.date.today()
        item_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=pickup_days)
        start_time = get_total_milliseconds(item_date)
        url = temp_url.format(item['venuesId'], start_time, item['skuId'])
        result = http_request(url)
    return result[0]


def print_result(obj_list):
    print_list = []
    for data in as_completed(obj_list):
        if isinstance(data.result(), list):
            for result in data.result():
                print_list.append(result)
        else:
            print_list.append(data.result())
    print_win(print_list)
    # print_wechat(print_list)


def print_wechat(print_list):
    if len(print_list) == 0:
        return
    print_temp = []

    for item in print_list:
        if item not in wechat_list:
            print_temp.append(item)
            wechat_list.append(item)
    if len(print_temp) == 0:
        return
    print_temp.sort(key=lambda x: (x['date'], x['site'], x['time']), reverse=False)
    date_list = groupby(print_temp, key=lambda x: (x['date']))
    double_num = 0
    uses = []

    for date, data_list in date_list:
        temp_time = datetime.timedelta(0)
        temp_time_list = []
        for item_time, time_list in groupby(data_list, key=lambda x: (x['time'])):
            time_arr = str(item_time).split(':')
            item_delta = datetime.timedelta(hours=int(time_arr[0]), minutes=int(time_arr[1]))
            temp = list(time_list)
            temp.sort(key=lambda x: (x['site']), reverse=False)
            if (item_delta - temp_time).total_seconds() == 3600:
                curr_num = len(temp) if len(temp) < len(temp_time_list) else len(temp_time_list)

                temp_time_list.sort(key=lambda x: (x['site']), reverse=False)
                for j in range(curr_num):
                    if temp_time_list[j] not in np.array(uses):
                        uses.append(temp_time_list[j])
                        double_num = double_num + 1
                    if temp[j] not in np.array(uses):
                        uses.append(temp[j])

            temp_time_list = temp
            temp_time = item_delta

    wechat_arr = []
    for i in range(len(print_temp)):
        if i == 0 or print_temp[i]['date'] != print_temp[i - 1]['date']:
            wechat_arr.append(
                '****日期:{},星期{}****'.format(print_temp[i]['date'],
                                                get_week_name(print_temp[i]['site_time'].isoweekday())))
        wechat_arr.append("时间段:{},场地号:{}".format(
            print_temp[i]['time'],
            print_temp[i]['site']))
    if double_num > 0:
        wechat_arr.append('****2小时+场地数量：{}****'.format(double_num))
    for i in range(len(uses)):
        if i == 0 or (i > 0 and uses[i]['date'] != uses[i - 1]['date']):
            wechat_arr.append(
                '****日期:{},星期{}****'.format(uses[i]['date'], get_week_name(uses[i]['site_time'].isoweekday())))
        wechat_arr.append("时间段:{},场地号:{}".format(
            uses[i]['time'],
            uses[i]['site']))
    send_msg(wechat_name, wechat_arr, names)


def print_win(print_list):
    if len(print_list) == 0:
        print('无空场地')
    print_list.sort(key=lambda x: (x['date'], x['site'], x['time']), reverse=False)
    uses = []
    for i in range(len(print_list) - 1):
        timedelta = print_list[i + 1]['site_time'] - print_list[i]['site_time']
        if abs(timedelta.total_seconds()) == 3600 \
                and print_list[i + 1] not in np.array(uses) \
                and print_list[i + 1]['date'] == print_list[i]['date']:
            uses.append(print_list[i])
            uses.append(print_list[i + 1])

    for i in range(len(print_list)):
        if i == 0 or print_list[i]['date'] != print_list[i - 1]['date']:
            print('*************日期：' + print_list[i]['date'])
        data_str = "日期:{},星期{},时间段:{},场地号:{}".format(
            print_list[i]['date'],
            get_week_name(print_list[i]['site_time'].isoweekday()),
            print_list[i]['time'],
            print_list[i]['site'])
        print("****************************************************" + data_str)
    print('2小时场地数量：{}'.format(int(len(uses) / 2)))
    uses_str = ''
    for i in range(len(uses)):
        if i > 0 and uses[i]['date'] != uses[i - 1]['date']:
            print('*************')
        data_str = '日期：{}，星期{}，时间段：{}，场地号：{}'.format(
            uses[i]['date'],
            get_week_name(uses[i]['site_time'].isoweekday()),
            uses[i]['time'],
            uses[i]['site'])
        print(
            '****************************************************' + data_str)

        uses_str = uses_str + data_str + '\n'
    if len(uses) > 0:
        requests.get(notice_url.format('2小时场地数量：{}'.format(int(len(uses) / 2)), uses_str), proxies=proxies,
                     verify="FiddlerRoot.pem")


def http_request(url):
    normals = []
    response = requests.get(url, proxies=proxies, verify="FiddlerRoot.pem")
    result_json = json.loads(response.content)
    if result_json is not None:
        for block in result_json['data']['modelList']:
            for block_item in block['blockModel']:
                if block_item['status'] == 1:
                    current = get_datetime(block['startTime'])
                    site_name = int((block_item['groundName']).replace('羽毛球', '').replace('号场', ''))
                    # if (np.array(sites) == site_name).any():
                    normals.append(
                        {
                            'site_time': current,
                            'date': current.strftime('%Y-%m-%d'),
                            'time': current.strftime('%H:%M'),
                            'site': site_name})

    return normals


def get_total_milliseconds(today):
    current = today - datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m-%d %H:%M')
    return int(current.total_seconds() * 1000)


def get_datetime(milliseconds):
    current = datetime.timedelta(milliseconds=milliseconds) + datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m'
                                                                                                             '-%d '
                                                                                                             '%H:%M')
    return current


def get_week_name(number):
    if number == 1:
        return '一'
    elif number == 2:
        return '二'
    elif number == 3:
        return '三'
    elif number == 4:
        return '四'
    elif number == 5:
        return '五'
    elif number == 6:
        return '六'
    elif number == 7:
        return '日'


def send_msg(friend_name, msg_arr, name_list):
    u = windll.LoadLibrary('user32.dll')
    result = u.GetForegroundWindow()
    if result == 0 or result == 67622:
        print('锁屏状态不能推送消息')
        pyautogui.press('enter')
        time.sleep(0.5)
        pyautogui.typewrite('2651')
        time.sleep(0.5)
    windll.user32.BlockInput(1)
    hwnd = win32gui.FindWindow("WeChatMainWndForPC", "微信")  # 获取窗口
    if win32gui.IsWindowVisible(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    if win32gui.IsIconic(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)

    time.sleep(0.5)
    # Ctrl + alt + w 打开微信
    # pyautogui.hotkey('ctrl', 'alt', 'w')

    for name_str in friend_name:
        # 搜索好友
        pyautogui.hotkey('ctrl', 'f')
        # 复制好友昵称到粘贴板
        pyperclip.copy(name_str)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 回车进入好友消息界面
        pyautogui.press('enter')
        time.sleep(1)
        # 复制需要发送的内容到粘贴板
        push_str = '#场地提醒：\n{}\n'.format('\n'.join(msg_arr))
        pyperclip.copy(push_str)
        # 模拟键盘 ctrl + v 粘贴内容
        pyautogui.hotkey('ctrl', 'v')
        for name in name_list:
            at_name(name)
        # 发送消息
        pyautogui.press('enter')
        time.sleep(1)
    # Ctrl + alt + w 关闭微信
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    windll.user32.BlockInput(0)


def at_name(name):
    pyautogui.typewrite('@' + name)
    pyautogui.press('enter')
    pyautogui.press('enter')
    time.sleep(0.1)


valid_coord = {0, 0}


def on_click(x, y, button, pressed):
    global valid_coord
    if pressed:
        valid_coord = (x, y)
        print('点击坐标{}，{}'.format(x, y))
        return False


if __name__ == '__main__':
    try:
        _main_()
    except:
        windll.user32.BlockInput(0)
        traceback.print_exc()
        print("按回车键退出")
        input()
    sys.exit()
