import base64
import datetime
import json
import os
import sys
import time
import warnings
from concurrent.futures import ThreadPoolExecutor, as_completed
from ctypes import windll

import pandas as pd
import pyautogui
import pyperclip
import requests
import schedule
import win32con
import win32gui
from pandas import DataFrame

from config import proxies, verify_str
from ddddocr import DdddOcr
from login.util import encrypt_pwd

ocr = DdddOcr()
public_key = "-----BEGIN PUBLIC KEY-----\n" + 'MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQUDdkHri8QotAJ/GqIZaxE1Vpv1b04LX3NCX64z3DSrAmL8iSHhimNnwOk0iPgI2TV50IKWjy0wLq+ziyMi27xAFvk8T0U1ma9aAn+qmmeKLNK9r0B9sv7Jvv0bbpA9z8sGChFLdf1V624T6s5xlJR2LD1hVIlG1S1s1cNYN6awIDAQAB\n' + "-----END PUBLIC KEY----- "

authCode_url = 'https://101.227.99.128:10443/security/getAuthCode'
login_url = 'https://101.227.99.128:10443/security/doLogin?lang=zh_CN'
get_mv_financing_list_url = 'https://101.227.99.128:10443/gmggt_api/routeBusiness/cbm/mvFinancing/getMVFinancingList'
get_pv_financing_list_url = 'https://101.227.99.128:10443/gmggt_api/pvFinancing/getPVFinancingList'
export_mv_financing_list_url = 'https://101.227.99.128:10443/gmggt_api/routeDownload/cbm/mvFinancing/exportMvFinancingList'
export_pv_financing_list_url = 'https://101.227.99.128:10443/gmggt_api/pvFinancing/exportPvFinancingList'

req = requests.session()
warnings.simplefilter('ignore')
risk_tip_changed_list = []
output_list = []
task_is_run = True


def _main_():
    # comparison_2()
    schedule_task()


def comparison_1():
    global req
    print('开始加载数据~')
    req = login('liujianhua', 'Ljh@152161')
    start = time.perf_counter()
    bath_task(get_pv_financing_list, 20, 2000, 2)
    end = time.perf_counter()
    print('get_pv_financing_list耗时：{:.4f}s'.format(end - start))
    start = time.perf_counter()
    bath_task(get_mv_financing_list, 20, 2000, 1)
    end = time.perf_counter()
    print('get_mv_financing_list耗时：{:.4f}s'.format(end - start))
    start = time.perf_counter()
    risk_changed_print()
    end = time.perf_counter()
    print('risk_changed_print耗时：{:.4f}s'.format(end - start))
    output_txt = '\n'.join(output_list)
    print(output_txt)
    save_txt(output_txt)


def comparison_2():
    global req, risk_tip_changed_list, output_list
    print('开始加载数据~')
    req = login('liujianhua', 'Ljh@152161')
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=None) as t:
        mv_obj = t.submit(export_mv_financing_list)
        pv_obj = t.submit(export_pv_financing_list)
    mv_print_list = []
    pv_print_list = []
    risk_tip_changed_list = []
    output_list = []
    if isinstance(mv_obj.result(), list):
        for result in mv_obj.result():
            mv_print_list.append(result)
    else:
        mv_print_list.append(mv_obj.result())

    if isinstance(pv_obj.result(), list):
        for result in pv_obj.result():
            pv_print_list.append(result)
    else:
        pv_print_list.append(pv_obj.result())
    print_result(mv_print_list, 1)
    print_result(pv_print_list, 2)
    end = time.perf_counter()
    print('加载数据耗时：{:.4f}s'.format(end - start))
    start = time.perf_counter()

    risk_changed_print()
    end = time.perf_counter()
    print('计算耗时：{:.4f}s'.format(end - start))
    # output_txt = '\n'.join(output_list)
    # print(output_txt)
    save_excel(output_list)
    # save_txt(output_txt)
    try:
        send_msg(['周婧'])
    except Exception as e:
        print('当日文件未发送')
        print(e.args)
    global task_is_run
    task_is_run = True


def risk_changed_print():
    change_none_1 = 0
    change_none_2 = 0
    change_none_3 = 0
    change_none_4 = 0
    change_up_1_1 = 0
    change_up_1_2 = 0
    change_up_2_1 = 0
    change_up_3_1 = 0
    change_up_3_2 = 0
    change_up_4_1 = 0
    error_num = 0
    for change in risk_tip_changed_list:
        try:
            if change['mvRiskTip'] == change['riskTip']:
                if change['riskTip'] == 5:
                    change_none_1 = change_none_1 + 1
                if change['riskTip'] == 4:
                    change_none_2 = change_none_2 + 1
                if change['riskTip'] == 2:
                    change_none_3 = change_none_3 + 1
                if change['riskTip'] == 0:
                    change_none_4 = change_none_4 + 1

            if change['mvRiskTip'] - change['riskTip'] == 1:
                if change['mvRiskTip'] == 2 and change['riskTip'] == 1:
                    change_up_1_1 = change_up_1_1 + 1
                if change['mvRiskTip'] == 1 and change['riskTip'] == 0:
                    change_up_1_2 = change_up_1_2 + 1
            if change['mvRiskTip'] - change['riskTip'] == 2:
                if change['mvRiskTip'] == 2 and change['riskTip'] == 0:
                    change_up_2_1 = change_up_2_1 + 1
            if change['mvRiskTip'] - change['riskTip'] == 3:
                if change['mvRiskTip'] == 4 and change['riskTip'] == 1:
                    change_up_3_1 = change_up_3_1 + 1
                if change['mvRiskTip'] == 3 and change['riskTip'] == 0:
                    change_up_3_2 = change_up_3_2 + 1
            if change['mvRiskTip'] - change['riskTip'] == 4:
                if change['mvRiskTip'] == 4 and change['riskTip'] == 0:
                    change_up_4_1 = change_up_4_1 + 1
        except Exception as e:
            error_num = error_num + 1
            print(e.args)
            print(change)
    print(error_num)

    output_list.append(
        {'column_0': '风险等级变动', 'column_1': '现状态', 'column_2': '新状态', 'column_3': '客户数', 'column_4': '风险应对'})

    output_list.append(
        {'column_0': '无变化', 'column_1': '资不抵债', 'column_2': '资不抵债', 'column_3': str(change_none_1),
         'column_4': '无变化，正常追债'})

    output_list.append(
        {'column_0': ' ', 'column_1': '平仓处置', 'column_2': '平仓处置', 'column_3': str(change_none_2), 'column_4': '停牌+退市'})

    output_list.append(
        {'column_0': ' ', 'column_1': '高风险', 'column_2': '高风险', 'column_3': str(change_none_3), 'column_4': '正常追保'})

    output_list.append(
        {'column_0': ' ', 'column_1': '安全', 'column_2': '安全', 'column_3': str(change_none_4), 'column_4': '无风险'})

    output_list.append(
        {'column_0': '上升一级', 'column_1': '中风险', 'column_2': '高风险', 'column_3': str(change_up_1_1), 'column_4': '开始追保'})

    output_list.append(
        {'column_0': ' ', 'column_1': '安全', 'column_2': '中风险', 'column_3': str(change_up_1_2), 'column_4': '无追保'})

    output_list.append(
        {'column_0': ' ', 'column_1': '安全', 'column_2': '高风险', 'column_3': str(change_up_2_1), 'column_4': '开始追保'})

    output_list.append(
        {'column_0': '上升三级', 'column_1': '中风险', 'column_2': '平仓处置', 'column_3': change_up_3_1,
         'column_4': '提示强平风险，若PV<86.25，两周豁免期'})

    output_list.append(
        {'column_0': ' ', 'column_1': '安全', 'column_2': '平仓预警', 'column_3': change_up_3_2,
         'column_4': '提示强平风险，平仓预警48H倒计时强平两周豁免期'})

    output_list.append(
        {'column_0': '上升四级', 'column_1': '安全', 'column_2': '平仓处置', 'column_3': change_up_4_1,
         'column_4': '提示强平风险，若PV<86.25，两周豁免期'})


def get_mv_financing_list(current, size):
    data = {"header": {"deviceId": "Chrome", "sysNo": "dchk_omp", "traceId": "d1c200190f96d24b9c88d0304b0b532e5474",
                       "transactionId": "", "userMark": ""}, "args": {"current": current, "size": size}}
    mv_financing_response = req.post(get_mv_financing_list_url, json=data, verify=verify_str, proxies=proxies)
    mv_financing_json = json.loads(mv_financing_response.content)
    return mv_financing_json['Data']['data']['records']


def get_pv_financing_list(current, size):
    data = {"header": {"deviceId": "Chrome", "sysNo": "dchk_omp", "traceId": "5708b2000bc76840061b68dc82c6a39a7f89",
                       "transactionId": "", "userMark": ""},
            "args": {"clientId": "", "visitStatus": "", "current": current, "size": size}}
    pv_financing_response = req.post(get_pv_financing_list_url, json=data, verify=verify_str, proxies=proxies)
    pv_financing_json = json.loads(pv_financing_response.content)
    return pv_financing_json['Data']['data']['records']


def export_mv_financing_list():
    data = {"header": {"deviceId": "Chrome", "sysNo": "hkcrm", "traceId": "6e43fca3b5e1e84bbbe99f823df58f677b7d",
                       "transactionId": "", "userMark": ""},
            "args": {"pageStart": "1", "pageEnd": "200", "size": "200"}}
    mv_financing_response = req.post(export_mv_financing_list_url, json=data, verify=verify_str, proxies=proxies)
    with open('mv_temp.xlsx', 'wb') as f:
        f.write(mv_financing_response.content)
        f.close()
    df = pd.read_excel('mv_temp.xlsx', sheet_name='导出结果', usecols=[1, 3, 5])
    rows = df.values
    mv_financing_list = []
    for row in rows:
        data = {
            'fundAccount': row[0],
            'mvRiskTip': row[1],
            'mvAmountInsured': row[2],
        }
        mv_financing_list.append(data)
    # os.remove('mv_temp.xlsx')
    return mv_financing_list


def export_pv_financing_list():
    data = {
        "header": {"deviceId": "Chrome", "sysNo": "hkcrm", "traceId": "7ab013c99427d549fb281b4f45bae76f2519",
                   "transactionId": "", "userMark": ""}, "args": {"pageStart": 1, "pageEnd": 200}}
    pv_financing_response = req.post(export_pv_financing_list_url, json=data, verify=verify_str, proxies=proxies)
    with open('pv_temp.xlsx', 'wb') as f:
        f.write(pv_financing_response.content)
        f.close()

    df = pd.read_excel('pv_temp.xlsx', sheet_name='导出结果', usecols=[1, 2, 4])
    rows = df.values
    pv_financing_list = []
    for row in rows:
        data = {
            'fundAccount': row[0],
            'riskTip': row[1],
            'amountInsured': row[2],
        }
        pv_financing_list.append(data)
    # os.remove('pv_temp.xlsx')
    return pv_financing_list


def bath_task(task, total_page, page_size, get_type):
    with ThreadPoolExecutor(max_workers=None) as t:
        obj_list = []
        for current in range(total_page):
            obj = t.submit(task, current, page_size)
            obj_list.append(obj)
    result_calc(obj_list, get_type)


def tip_input(item, risk_tip, risk_tip_int):
    index = next((i for i, x in enumerate(risk_tip_changed_list) if x['fundAccount'] == item['fundAccount']),
                 None)
    if index is None:
        risk_tip_changed_list.append({'fundAccount': item['fundAccount'], risk_tip: risk_tip_int})
    else:
        risk_tip_changed_list[index][risk_tip] = risk_tip_int


def print_result(print_list, get_type):
    # mv不同风险状态的数据集合
    overdraft_mv_list = []
    close_mv_list = []
    warn_close_mv_list = []
    press_mv_list = []
    warning_mv_list = []
    normal_mv_list = []
    # mv客户数量
    total_overdraft_mv = 0
    total_close_mv = 0
    total_warn_close_mv = 0
    total_press_mv = 0
    total_warning_mv = 0
    total_normal_mv = 0
    # mv追保金额
    overdraft_mv_insured = 0
    close_mv_insured = 0
    warn_close_mv_insured = 0
    press_mv_insured = 0
    warning_mv_insured = 0
    normal_mv_insured = 0
    total = 0
    total_insured = 0
    riskTip = 'mvRiskTip' if get_type == 1 else 'riskTip'
    title = 'MV' if get_type == 1 else 'PV'
    amountInsured = 'mvAmountInsured' if get_type == 1 else 'amountInsured'
    for item in print_list:
        total = total + 1
        total_insured = total_insured + float(item[amountInsured])
        if item[riskTip] == "资不抵债":
            total_overdraft_mv = total_overdraft_mv + 1
            overdraft_mv_insured = overdraft_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 5)
            overdraft_mv_list.append(item)
            continue
        if item[riskTip] == "平仓处置":
            total_close_mv = total_close_mv + 1
            close_mv_insured = close_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 4)
            close_mv_list.append(item)
            continue
        if item[riskTip] == "平仓预警":
            total_warn_close_mv = total_warn_close_mv + 1
            warn_close_mv_insured = warn_close_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 3)
            warn_close_mv_list.append(item)
            continue
        if item[riskTip] == "高风险":
            total_press_mv = total_press_mv + 1
            press_mv_insured = press_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 2)
            press_mv_list.append(item)
            continue
        if item[riskTip] == "中风险":
            total_warning_mv = total_warning_mv + 1
            warning_mv_insured = warning_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 1)
            warning_mv_list.append(item)
            continue
        if item[riskTip] == "安全":
            total_normal_mv = total_normal_mv + 1
            normal_mv_insured = normal_mv_insured + float(item[amountInsured])
            tip_input(item, riskTip, 0)
            normal_mv_list.append(item)
    # print_txt.append(title + '风险等级'.ljust(14, ' ') + '客户数'.ljust(17, ' ') +
    #                  '客户数量占比'.ljust(14, ' ') + '追保金额'.ljust(16, ' ') +
    #                  '追保金额占比'.ljust(14, ' '))
    output_list.append(
        {'column_0': '风险等级', 'column_1': '客户数', 'column_2': '客户数量占比', 'column_3': '追保金额', 'column_4': '追保金额占比'})
    print_data('安全', total_normal_mv, total, normal_mv_insured, total_insured)
    print_data('中风险', total_warning_mv, total, warning_mv_insured, total_insured)
    print_data('高风险', total_press_mv, total, press_mv_insured, total_insured)
    print_data('平仓预警', total_warn_close_mv, total, warn_close_mv_insured, total_insured)
    print_data('平仓处置', total_close_mv, total, close_mv_insured, total_insured)
    print_data('资不抵债', total_overdraft_mv, total, overdraft_mv_insured, total_insured)
    # print_txt.append('**************')


def save_txt(txt):
    if not os.path.exists('log'):
        os.mkdir('log')
    path = 'log\\' + datetime.date.today().strftime('%Y%m%d') + '.txt'
    with open(path, 'w') as ws:
        ws.write(txt + '\n')
        ws.close()


def save_excel(excel_list):
    if not os.path.exists('log'):
        os.mkdir('log')
    path = 'log\\' + datetime.date.today().strftime('%Y%m%d') + '.xlsx'
    df = pd.DataFrame.from_dict(excel_list)
    df.to_excel(path, index=False, header=False, encoding='utf-8')


def result_calc(obj_list, get_type):
    print_list = []
    for data in as_completed(obj_list):
        if isinstance(data.result(), list):
            for result in data.result():
                print_list.append(result)
        else:
            print_list.append(data.result())
    print_result(print_list, get_type)


def print_data(tip, data, total_data, insured, total_insured):
    # print_txt.append(
    #     '{}{}{}{}{}'.format(tip.ljust(20 - len(tip), ' '), str(data).ljust(20, ' '),
    #                         (str(round(data / total_data * 100, 2)) + '%').ljust(20, ' '),
    #                         str(round(insured, 2)).ljust(20, ' '),
    #                         (str(round(insured / total_insured * 100, 2)) + '%').ljust(20, ' ')))
    output_list.append(
        {'column_0': tip, 'column_1': data, 'column_2': (str(round(data / total_data * 100, 2)) + '%'),
         'column_3': str(round(insured, 2)), 'column_4': str(round(insured / total_insured * 100, 2)) + '%'})


# 登录
def login(user_id, pwd):
    login_num = 0

    # 登录
    while login_num < 10:
        code_response = req.post(authCode_url, verify=verify_str, proxies=proxies, json={})
        code_json = json.loads(code_response.content)
        pic_data = base64.b64decode(code_json['data']['pictureCheckCode'])
        code = ocr.classification(pic_data)

        data = {"header": {"deviceId": "Chrome",
                           "sysNo": "dchk_omp",
                           "traceId": "c01bd6fb0df4f341c3ea050b929f9babdd63",
                           "transactionId": "",
                           "userMark": ""},
                "args": {
                    "password": encrypt_pwd(pwd, public_key),
                    "username": user_id,
                    "productEid": 1,
                    "timeout": "20",
                    "region": "0",
                    "pictureCheckCode": code,
                    "pictureCheckKey": code_json['data']['pictureCheckKey'],
                    "url": "/doLogin?lang=zh_CN"}}

        login_response = req.post(login_url, json=data, verify=verify_str, proxies=proxies)
        login_json = json.loads(login_response.content)
        if login_json['success'] is False:
            login_num = login_num + 1
        else:
            req.params = {'user_name': login_json['data']['realName']}
            return req

    return None


def schedule_task():
    # 每天17:50执行
    schedule.every().day.at("17:30").do(comparison_2)
    global task_is_run
    while True:
        if task_is_run:
            task_is_run = False
            print("下次运行时间：{}".format(schedule.next_run()))
        schedule.run_pending()
        time.sleep(1)


def send_msg(friend_name):
    u = windll.LoadLibrary('user32.dll')
    result = u.GetForegroundWindow()
    if result == 0 or result == 67622:
        print('锁屏状态不能推送消息')
        return
    windll.user32.BlockInput(1)
    time.sleep(0.5)
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_1", "咚咚")  # 获取窗口
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
        find_img('img\\search.png')
        # 复制好友昵称到粘贴板
        pyperclip.copy(name_str)
        # 模拟键盘 ctrl + v 粘贴
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        # 回车进入好友消息界面
        pyautogui.press('enter')
        time.sleep(1)
        # 复制需要发送的内容到粘贴板
        find_img('img\\file_send.png')
        path = os.getcwd() + '\\log\\' + datetime.date.today().strftime('%Y%m%d') + '.xlsx'
        pyperclip.copy(path)
        # 模拟键盘 ctrl + v 粘贴内容
        pyautogui.hotkey('ctrl', 'v')
        # 发送消息
        pyautogui.press('enter')
        time.sleep(1)
    # Ctrl + alt + w 关闭微信
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
    windll.user32.BlockInput(0)


def find_img(img):
    image_l = pyautogui.locateOnScreen(img, grayscale=True)
    center = pyautogui.center(image_l)
    pyautogui.click(center, interval=0.1, clicks=1, duration=0.1)


if __name__ == '__main__':
    try:
        _main_()
    except Exception as ex:
        windll.user32.BlockInput(0)
        print(ex.args)
        print(ex.strerror)
        print(ex.errno)
    input('任意键退出')
    sys.exit()
