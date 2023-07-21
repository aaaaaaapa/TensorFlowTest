import datetime
import json
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

import requests
import random
from lxml import etree
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_random_ua():  # 随机UA
    ua = UserAgent()
    return ua.random


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Content-Type": "application/json",
    "Cookie": 'SESSION=YzYzYzk5OWMtN2I0ZC00OGJjLWIzZjgtMzA4ZTYzZjU4YjI2; CRM_API_TOKEN=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX3Rva2VuX2luZm8iOnsidXNlcklkIjoiMjEzMDAwMTQ5OTY1MTU3NjY1IiwicHJvZHVjdElkIjoiMjEzMDAwMTM4MDM1NTQ3NzI4IiwiZGV2aWNlIjoiQ2hyb21lIiwidGltZW91dCI6MTIwMCwic3lzTm8iOiJkY2hrX29tcCJ9LCJpYXQiOjE2NjAwNDE0Mjd9.pAdjSiyeaVUVgjrRv8vrUDZaAc9wZcMCrX3ei9qEVMooYoWzomfFRtvA6NGEobnjHG8Mu0x910UbZLuZcE-Y2A',
    "dchktoken": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJ1c2VyX3Rva2VuX2luZm8iOnsidXNlcklkIjoiMjEzMDAwMTQ5OTY1MTU3NjY1IiwicHJvZHVjdElkIjoiMjEzMDAwMTM4MDM1NTQ3NzI4IiwiZGV2aWNlIjoiQ2hyb21lIiwidGltZW91dCI6MTIwMCwic3lzTm8iOiJkY2hrX29tcCJ9LCJpYXQiOjE2NjAwNDE0Mjd9.pAdjSiyeaVUVgjrRv8vrUDZaAc9wZcMCrX3ei9qEVMooYoWzomfFRtvA6NGEobnjHG8Mu0x910UbZLuZcE-Y2A"
}

url = 'https://www.nihaowua.com/'
proxies = []
proxies_num=5

def get_ip_list(url, headers):
    web_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[0].text + ':' + tds[1].text)
    return ip_list


def get_random_ip():
    if len(proxies) == 0:
        return None
    proxy_ip = random.choice(proxies)
    proxy = json.load(proxy_ip)
    return proxy


def bath_get_proxies():  # 随机IP
    agent_url = 'https://www.kuaidaili.com/free/inha/'
    # url = 'https://www.kuaidaili.com/free/'
    proxies_list = []
    with ThreadPoolExecutor(max_workers=5) as t:
        obj_list = []
        for i in range(proxies_num):
            obj = t.submit(get_proxies, i)
            obj_list.append(obj)
    for i in range(10):
        time.sleep(5)
        for obj in obj_list:
            if obj.done() is False:
                break


def get_proxies(index):
    global proxies
    if index != 0:
        agent_url = 'https://www.kuaidaili.com/free/inha/{}'.format(str(index) + '/')
    ip_list = get_ip_list(agent_url, headers=headers)
    for ip in ip_list:
        proxies.append({'http': 'http://' + ip})


def main_print():  # 直接打印输出程序
    count = 0
    while True:
        data = {"exchange_type": "K", "_t": 1660046466}
        res = requests.post("https://101.227.99.128:10443/gmggt_api/common/getTradeDaysResponse", headers=headers,
                            json=data)
        res.encoding = 'utf-8'
        selector = etree.HTML(res.text)
        xpath_reg = "//section/div/*/text()"
        results = selector.xpath(xpath_reg)
        content = results[0]
        count += 1
        print('********正在爬取中，这是第{}次爬取********'.format(count))
        print(content)


def main_keep():  # 写入txt文本程序
    count = 0
    requests.packages.urllib3.disable_warnings()
    with open("NiHaoWu.txt", "a") as f:
        while True:
            res = requests.get(url=url, headers=headers, verify=False, proxies=get_random_ip())
            res.encoding = 'utf-8'
            selector = etree.HTML(res.text)
            xpath_reg = "//section/div/*/text()"
            results = selector.xpath(xpath_reg)
            content = results[0]
            f.write(content + '\n')
            count += 1
            print('********正在爬取中，这是第{}次爬取********'.format(count))
            time.sleep(1)


if __name__ == '__main__':
    file_path = 'proxies' + datetime.datetime.today().strftime('%Y-%m-%d') + '.txt'
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf8') as f:
            proxies = f.readlines()
            f.close()
    else:
        bath_get_proxies()
        with open(file_path, "a") as f:
            f.writelines(json.dump(proxies))
            f.close()
    main_keep()
