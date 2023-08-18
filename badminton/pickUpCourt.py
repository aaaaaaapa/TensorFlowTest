# author: yf
# date: 2022/11/05 16:12
import datetime
import json
import os
import random
import sqlite3
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from ctypes import windll
from itertools import groupby

import numpy as np
import pyautogui
import pyperclip
import requests
import schedule
import urllib3
import win32con
import win32gui
from bs4 import BeautifulSoup
from chinese_calendar import is_holiday

temp_url = "https://user.jusssportsvenue.com/api/block/ground/list?venuesId={}&sportsType=9&startTime={}&skuId={}&_t={}"
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'
group_param = [
    {'venuesId': 30, 'skuId': 35},
    {'venuesId': 30, 'skuId': 36},
    {'venuesId': 30, 'skuId': 37},
    {'venuesId': 27, 'skuId': 38},
]
timespans = ['1830', '1900', '1930', '2000']
week_timespans = ['1300', '1330', '1400', '1430', '1500', '1530', '1600', '1630', '1700', '1730', '1800', '1830',
                  '1900', '1930', '2000']
random_start = 10
random_end = 20
wechat_list = []
wechat_name = []
names = []
proxies = []
# proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
begin_time = None
verify_str = "FiddlerRoot.pem"
is_agent = True
task_is_run = True
urllib3.disable_warnings()
timing_days = 6
proxies_num = 50
agent_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}
user_agent_list = [
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) Gecko/20100101 Firefox/61.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10.5; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15",
]
db_file_path = ''
day_n = '1'


def get_ip_list(url):
    web_data = requests.get(url, headers=agent_headers)

    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    return ip_list


def get_proxies(index):
    global proxies
    agent_url = 'https://www.kuaidaili.com/free/inha/'
    if index != 0:
        agent_url = 'https://www.kuaidaili.com/free/inha/{}'.format(str(index) + '/')
    ip_list = get_ip_list(agent_url)
    for ip in ip_list:
        proxies.append(json.dumps({'http': 'http://' + ip}))


def bath_get_proxies():  # 随机IP
    agent_url = 'https://www.kuaidaili.com/free/inha/'
    # url = 'https://www.kuaidaili.com/free/'
    proxies_list = []
    for i in range(proxies_num):
        get_proxies(i)
        interval = float(random.randint(1, 30)) / 10
        print('当前页数{},间隔{}秒'.format(str(i), str(interval)))
        time.sleep(interval)


def refush_proxy_file(file_path):
    global proxies
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf8') as f:
            proxies = f.readlines()
            for i in range(len(proxies)):
                proxies[i] = proxies[i].replace('\n', '')

            f.close()
    else:
        bath_get_proxies()
        with open(file_path, "a") as f:
            for pro in proxies:
                f.write(pro + '\n')
            f.close()


def _main_():
    global timespans, week_timespans, random_start, random_end, wechat_name, names, wechat_list, is_agent, db_file_path, day_n

    file_path = 'proxies' + datetime.datetime.today().strftime('%Y-%m-%d') + '.txt'
    refush_proxy_file(file_path)
    with open("config.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    if len(configList) != 8:
        print('配置文件错误！')
        input('输入任意键退出')
        sys.exit()
    for config in configList:
        if config.startswith('时间段'):
            timespans = config.replace('\n', '').split('=')[1].split(',')
        if config.startswith('周末时间段'):
            week_timespans = config.replace('\n', '').split('=')[1].split(',')
        if config.startswith('搜索间隔时间'):
            intervalArr = config.replace('\n', '').split('=')[1].split('-')
            random_start = int(intervalArr[0])
            random_end = int(intervalArr[1])
        if config.startswith('群名称'):
            name_str = config.replace('\n', '').split('=')[1]
            if name_str != '':
                wechat_name = name_str.split(',')

        if config.startswith('艾特人名拼音'):
            temp = config.replace('\n', '').split('=')[1]
            if temp.strip() != '':
                names = temp.split(',')
        if config.startswith('是否代理'):
            agent_str = config.replace('\n', '').split('=')[1]
            is_agent = agent_str == '1'
        if config.startswith('数据库路径'):
            db_file_path = config.replace('\n', '').split('=')[1]
        if config.startswith('监测几天后的数据'):
            day_n = config.replace('\n', '').split('=')[1]

    clear_index = 0
    wechat_list = []
    exec_time = '12:00'

    temp_time = datetime.datetime.strptime(exec_time, '%H:%M')
    while True:
        if clear_index > 100:
            clear_index = 0
            wechat_list = []

        windll.user32.BlockInput(0)
        curr_date = datetime.datetime.today()
        temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
        diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
        if 0 < diff_seconds < 20:
            print('12点数据收集中，等待{}秒'.format(str(diff_seconds + 0.01)))
            time.sleep(diff_seconds + 0.01)
            exec_search(True)
        else:
            exec_search(False)

        current_random = random.randint(random_start * 1000, random_end * 1000)
        print('等待{}毫秒，重新搜索~'.format(current_random))
        time.sleep(current_random / 1000)
        clear_index = clear_index + 1


def exec_search(is_current):
    global begin_time

    print("{}开始搜索{}空闲场地~~".format(datetime.datetime.now(), '整点' if is_current else '常规'))

    windll.user32.BlockInput(0)
    obj_list = []
    begin_time = datetime.datetime.now()
    with ThreadPoolExecutor(max_workers=None) as t:
        for i in range(7):
            if datetime.datetime.now().hour < 12 and i == 6:
                continue
            if i < int(day_n):
                continue
            if is_current is True:
                if i != timing_days:
                    continue
                else:
                    print("{}开始搜索空闲场地~~12点场地".format(datetime.datetime.now()))
            for item in group_param:
                start_times = []
                today = datetime.datetime.today()
                item_date = datetime.datetime(today.year, today.month, today.day) + datetime.timedelta(days=i + 1)
                temp = week_timespans if is_holiday(item_date) else timespans
                for timespan in temp:
                    start_times.append(
                        get_total_milliseconds(item_date +
                                               datetime.timedelta(hours=int(timespan[0:2]),
                                                                  minutes=int(timespan[2:4]))))
                start_time = get_total_milliseconds(item_date)
                url = temp_url.format(item['venuesId'], start_time, item['skuId'], time.perf_counter())
                obj = t.submit(http_request, url, start_times)
                obj_list.append(obj)

        print_result(obj_list, is_current)


def print_result(obj_list, is_current):
    global task_is_run
    print_list = []
    for data in as_completed(obj_list):
        if isinstance(data.result(), list):
            for result in data.result():
                print_list.append(result)
        else:
            print_list.append(data.result())
    interval = datetime.datetime.now() - begin_time
    print('{},搜索用时：{}毫秒'.format(datetime.datetime.now(), int(interval.total_seconds() * 1000)))
    print_win(print_list)
    print_wechat(print_list, is_current)
    if is_current:
        task_is_run = True


def print_wechat(print_list, is_current):
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
    if len(wechat_arr) > 0:
        wechat_arr.insert(0, "时间点:{}".format(datetime.datetime.now()))
        write_txt_real(wechat_arr)
    if len(wechat_name) != 0:
        send_msg(wechat_name, wechat_arr, names)
    if is_current:
        write_txt(wechat_arr)


def write_txt(log):
    curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(curr_date_str + 'log.txt', 'w', encoding='utf8') as w:
        w.write("\n".join(log))
        w.write('\n')
        w.close()


def write_txt_real(log):
    curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(curr_date_str + 'real_log.txt', 'a+', encoding='utf8') as w:
        w.write("\n".join(log)+'\n')
        w.close()


def print_win(print_list):
    if len(print_list) == 0:
        print('无空场地')
    print_list.sort(key=lambda x: (x['date'], x['site'], x['time']), reverse=False)
    uses = []
    signal_list = []
    if len(print_list) == 1:
        signal_list.append(print_list[0])
    else:
        for i in range(len(print_list) - 1):
            timedelta = print_list[i + 1]['site_time'] - print_list[i]['site_time']
            if abs(timedelta.total_seconds()) == 3600 \
                    and print_list[i + 1] not in np.array(uses) \
                    and print_list[i + 1]['date'] == print_list[i]['date'] \
                    and print_list[i + 1]['site'] == print_list[i]['site']:
                uses.append(print_list[i])
                uses.append(print_list[i + 1])
            elif print_list[i] not in np.array(uses):
                signal_list.append(print_list[i])

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
    insert_court(uses, signal_list)


# request_get(notice_url.format('2小时场地数量：{}'.format(int(len(uses) / 2)), uses_str))


def request_get(url):
    for i in range(5):
        try:
            if is_agent:
                return requests.get(url, proxies=get_random_ip(), verify=False, stream=True,
                                    headers={'User-Agent': random.choice(user_agent_list)}, timeout=5)
            else:

                return requests.get(url, verify=False, stream=True, timeout=5)
        except:
            traceback.print_exc()
            continue


def get_random_ip():
    if len(proxies) == 0:
        return None
    proxy_ip = random.choice(proxies)
    proxy = json.loads(proxy_ip)
    return proxy


def http_request(url, start_times):
    normals = []
    response = request_get(url)
    result_json = json.loads(response.content)
    if result_json is not None:
        for block in result_json['data']['modelList']:
            if (np.array(start_times) == block['startTime']).any():
                for block_item in block['blockModel']:
                    if block_item['status'] == 1:
                        current = get_datetime(block['startTime'])
                        site_name = int((block_item['groundName']).replace('羽毛球', '').replace('号场', ''))
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


def schedule_task(exec_time):
    # 每天exec_time执行
    temp_time = datetime.datetime.strptime(exec_time, '%H:%M')
    schedule.every().day.at(exec_time).do(exec_search, is_current=True)
    # schedule.every(30).seconds.do(exec_search, is_current=False)
    global task_is_run
    while True:
        if task_is_run:
            task_is_run = False
            print("下次运行时间：{}".format(schedule.next_run()))

        schedule.run_pending()
        interval = 1
        curr_date = datetime.datetime.today()
        temp_time = datetime.datetime(curr_date.year, curr_date.month, curr_date.day, temp_time.hour, temp_time.minute)
        diff_seconds = (temp_time - datetime.datetime.now()).total_seconds()
        if diff_seconds < 30:
            interval = 0.01
        time.sleep(interval)


def conn_sqlite():
    return sqlite3.connect(db_file_path)


def create_court_table():
    conn = conn_sqlite()
    c = conn.cursor()
    c.execute('''CREATE TABLE jiushi_court
           (ID INTEGER PRIMARY KEY AUTOINCREMENT,-- 主键
           COURT_DATE           TEXT    NOT NULL,-- 日期
           COURT_SITE            TEXT     NOT NULL,-- 场地号
           COURT_TIME        TEXT    NOT NULL,-- 时间段
           COURT_STATUS         int NOT NULL,-- 状态 0、闲置；1、抢购中；2、成功；3、失败；4、过期
           BUY_ACCOUNT      TEXT NOT NULL, -- 抢购的微信账号
           APPEAR_TIME      TEXT    NOT NULL, -- 出现的时间
           COURT_NO             TEXT NOT NULL -- 场地编号
           );''')
    print("数据表创建成功")
    conn.commit()
    conn.close()


def insert_court(court_list, sign_list):
    conn = conn_sqlite()
    c = conn.cursor()
    c.execute('DELETE FROM jiushi_court WHERE court_status in (0,1) ')
    if len(court_list) != 0:
        uses = []
        for i in range(len(court_list) - 1):
            timedelta = court_list[i + 1]['site_time'] - court_list[i]['site_time']
            if abs(timedelta.total_seconds()) == 3600 \
                    and court_list[i + 1] not in np.array(uses) \
                    and court_list[i + 1]['date'] == court_list[i]['date'] \
                    and court_list[i + 1]['site'] == court_list[i]['site']:
                uses.append(court_list[i])
                uses.append(court_list[i + 1])
                court_time = str(court_list[i]['time']).replace(':00', '').replace(':30', '') + ',' + str(
                    court_list[i + 1]['time']).replace(':00', '').replace(':30', '')
                court_no = court_list[i]['date'] + str(court_list[i]['site']) + court_time
                c.execute("INSERT INTO jiushi_court (COURT_DATE,COURT_SITE,COURT_TIME,COURT_STATUS,BUY_ACCOUNT,APPEAR_TIME,COURT_NO) \
                      VALUES ('{}', '{}','{}',{},'{}','{}','{}')".format(court_list[i]['date'], court_list[i]['site'],
                                                                         court_time, 0,
                                                                         '', str(datetime.datetime.now()),
                                                                         court_no))
    # if len(sign_list) > 0:
    #     for sign in sign_list:
    #         court_time = str(sign['time']).replace(':00', '').replace(':30', '')
    #         court_no = sign['date'] + str(sign['site']) + str(sign['time']).replace(':00', '').replace(':30', '')
    #         c.execute("INSERT INTO jiushi_court (COURT_DATE,COURT_SITE,COURT_TIME,COURT_STATUS,BUY_ACCOUNT,APPEAR_TIME,COURT_NO) \
    #                               VALUES ('{}', '{}','{}',{},'{}','{}','{}')".format(sign['date'],
    #                                                                                  sign['site'],
    #                                                                                  court_time, 0,
    #                                                                                  '', str(datetime.datetime.now()),
    #                                                                                  court_no))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    while True:
        try:
            _main_()
        except:
            windll.user32.BlockInput(0)
            traceback.print_exc()
        time.sleep(5)
