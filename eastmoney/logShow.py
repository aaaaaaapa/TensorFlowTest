import datetime
import json
import os
import sys
import time
from io import BytesIO

from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import win32api

from ddddocr import DdddOcr

ocr = DdddOcr()
service = Service(r'C:\Users\Administrator\PycharmProjects\TensorFlowTest\venv\Scripts\chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = 'http://180.163.42.202:18000/login/?t=1661233009.706505&sr=log'


# 每日风控数据比对自动获取
def _main_():
    driver.get(url)
    # 账号填充输入

    elem_user = driver.find_element(By.NAME, 'login')
    elem_psw = driver.find_element(By.NAME, 'pwd')
    elem_code = driver.find_element(By.NAME, 'code')

    # 点击查看验证码
    click_code = driver.find_element(By.XPATH, "//img[@id='verifycodeimg']")
    while True:
        click_code.click()
        time.sleep(1)
        location = click_code.location
        size = click_code.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        img = Image.open(BytesIO(driver.get_screenshot_as_png())).crop((left, top, right, bottom))
        cap = ocr.classification(img)
        print('code:' + cap)
        elem_code.send_keys(cap)
        # 可以自己修改登录名和账户密码，我自己的隐去了
        elem_user.send_keys('yanfeng')
        # 5e6xGe6e
        elem_psw.send_keys('5e6xGe6e')

        # 点击登录
        click_login = driver.find_element(By.XPATH, "//input[@value='登录']")
        click_login.click()
        time.sleep(2)
        # 点击跳转到日志查询
        click_log = driver.find_element(By.XPATH, "//div[contains(@onclick,'go_new_url')]")
        if click_log is None:
            continue
        else:
            click_log.click()
            time.sleep(2)
            break

    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        if '日志检索' in driver.title:
            break
    # 日志检索
    click_search = driver.find_element(By.XPATH, "// a[contains( @ href, 'log_search_init')]")
    click_search.click()
    time.sleep(1)
    # 查询孖展是否一致
    click_2 = driver.find_element(By.XPATH, "//button[contains(text(),'2')]")
    click_2.click()
    time.sleep(1)
    ele_margin = driver.find_element(By.XPATH, "//span[contains(text(),'孖展不一致数量')]")
    txt_margin = ele_margin.text
    # 查询具体不相等数量
    driver.find_element(By.XPATH, "//button[contains(text(),'1')]").click()
    time.sleep(1)
    # 把txt输出到文本
    text_diff = driver.find_element(By.XPATH, "//span[contains(text(),'具体不相等数量')]")
    arr_diff = text_diff.text.split(',')
    diff = json.loads(text_diff.text.replace('具体不相等数量:', ''))
    if diff['ipo_freez'] > 0:
        arr_diff[0] = (arr_diff[0] + ',').ljust(30, ' ')
    if diff['mv_risk_tip'] > 0:
        arr_diff[1] = (arr_diff[1] + ',').ljust(30, ' ') + 'mv_rate值不一致'
    if diff['margin_pv_amount_insured'] > 0:
        arr_diff[2] = (arr_diff[2] + ',').ljust(30, ' ') + '偏差<0.05'
    if diff['margin_pv_risk_tip'] > 0:
        arr_diff[3] = (arr_diff[3] + ',').ljust(30, ' ') + 'margin_pv_rate值不一致'
    if diff['mv_rate'] > 0:
        arr_diff[4] = (arr_diff[4] + ',').ljust(30, ' ') + 'market_value_mortgage值不一致'
    if diff['security_value'] > 0:
        arr_diff[5] = (arr_diff[5] + ',').ljust(30, ' ') + '股票价格不一致'
    if diff['amount_credit'] > 0:
        arr_diff[6] = (arr_diff[6] + ',').ljust(30, ' ') + '老风控不准确'
    if diff['amount_liabilities'] > 0:
        arr_diff[7] = (arr_diff[7] + ',').ljust(30, ' ') + '有问题需要查询详情'
    if diff['risk_tip'] > 0:
        arr_diff[9] = (arr_diff[9] + ',').ljust(30, ' ') + 'pv_rate值不一致'
    if diff['amount_insured'] > 0:
        arr_diff[10] = (arr_diff[10] + ',').ljust(30, ' ') + '偏差<0.05'
    if diff['mv_amount_insured'] > 0:
        arr_diff[12] = (arr_diff[12] + ',').ljust(30, ' ') + 'mv_rate值不一致'
    if diff['net_assets'] > 0:
        arr_diff[13] = (arr_diff[13] + ',').ljust(30, ' ') + 'security_value值不一致'
    if diff['market_value_mortgage'] > 0:
        arr_diff[15] = (arr_diff[15] + ',').ljust(30, ' ') + '股票价格不一致'
    if diff['margin_pv_rate'] > 0:
        arr_diff[16] = (arr_diff[16] + ',').ljust(30, ' ') + 'security_value值不一致'
    if diff['pv_rate'] > 0:
        arr_diff[17] = (arr_diff[17] + ',').ljust(30, ' ') + 'security_value值不一致'
    if diff['ipo_cut'] > 0:
        arr_diff[18] = (arr_diff[18] + ',').ljust(30, ' ') + '老风控不准确'
    path = '../log/' + datetime.date.today().strftime('%Y%m%d') + '.txt'
    with open(path, 'w') as ws:
        ws.write('今日风控比对结果：\n')
        for risk_str in arr_diff:
            ws.write(risk_str + '\n')
        ws.write(txt_margin)
        ws.close()
    # 查询具体不相等数量
    driver.find_element(By.XPATH, "//button[contains(text(),'3')]").click()

    price_list = []
    btn_name = '下页'
    while True:
        time.sleep(1)
        ele_total = driver.find_element(By.XPATH, "//span[contains(text(), '第')]")
        first = str.strip(ele_total.text[ele_total.text.find('至') + 1: ele_total.text.find('条')])
        total = str.strip(ele_total.text[ele_total.text.find('共') + 1: ele_total.text.rfind('条')])
        if str.strip(ele_total.text[ele_total.text.find('第') + 1: ele_total.text.find('至')]) == '1':
            btn_name = '下页'
        if int(first) == int(total):
            btn_name = '上页'
        # 把txt输出到文本
        price_diffs = driver.find_elements(By.XPATH, "//span[contains(text(),'股票价格')]")

        for price_diff in price_diffs:
            if '股票价格不一致数量' in price_diff.text:
                continue
            else:
                txt = price_diff.text.replace('自研股票价格为空：', '').replace('股票价格不一致：', '').replace('exchange_type:',
                                                                                               '').replace('币种：',
                                                                                                           '').replace(
                    '恒生：', '').replace('自研：', '').split(',')
                if len(txt) == 5:
                    data = {'stk_code': txt[0], 'exchange_type': txt[1], 'money_type': txt[2], 'hs_price': txt[3],
                            'em_price': txt[4]}
                if len(txt) == 4:
                    data = {'stk_code': txt[0], 'exchange_type': txt[1], 'money_type': '', 'hs_price': txt[2],
                            'em_price': txt[3]}
                diff = [x for x in price_list if x['stk_code'] == data['stk_code']]
                if len(diff) == 0:
                    price_list.append(data)

        if len(price_list) + 1 == int(total):
            break

        driver.find_element(By.XPATH, "//a[contains(text(),'{}')]".format(btn_name)).click()
        time.sleep(0.5)
    price_list.sort(key=lambda x: x['stk_code'], reverse=True)
    with open('../price.txt', 'w') as w:
        for stk in price_list:
            # if stk['stk_code'][0:2] != 'HK' and float(stk['em_price']) == 0:
            # sql = "update em_secuhk.price set asset_price={} where stock_code='{}' and asset_price={}".format(
            #     stk['hs_price'], stk['stk_code'], stk['em_price'])
            # if float(stk['price']) != 0 and stk['exchange_type'] != 'm':
            sql = 'stk_code:' + stk['stk_code'].ljust(20, ' ') + ',' \
                  + 'exchange_type:' + stk['exchange_type'].ljust(2, ' ') + ',' \
                  + 'money_type:' + stk['money_type'].ljust(2, ' ') + ',' \
                  + 'hs_price:' + stk['hs_price'].ljust(20, ' ') + ',' \
                  + 'em_price:' + stk['em_price'].ljust(20, ' ')
            # sql = "insert into em_secuhk.price (exchange_type, stock_code, init_date, asset_price, last_price, money_type)values ('{}','{}',{},{},{},'{}');".format(
            #     stk['exchange_type'], stk['stk_code'], datetime.date.today().strftime('%Y%m%d'), stk['price'],
            #     stk['price'], stk['money_type']
            # )
            # sql = "'" + stk['stk_code'] + "'"
            w.write(sql + '\n')
        w.close()
    driver.quit()
    service.stop()
    time.sleep(0.1)
    # os.system(r'start "" /d "C:\Program Files (x86)\Notepad++" /wait "notepad++.exe" "./log/20220824.txt"')
    win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Notepad++\notepad++.exe', path, '', 1)
    sys.exit()


if __name__ == '__main__':
    try:
        _main_()
    except Exception as ex:
        print(ex)
        driver.quit()
        service.stop()
        sys.exit()
