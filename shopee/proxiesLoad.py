import datetime
import json
import os
import random
import time

import requests
from bs4 import BeautifulSoup

proxies_num = 50
agent_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}
proxies = []


def del_proxy_file(file_path):
    for root, dirs, files in os.walk(file_path):
        for name in files:
            if 'proxies' in name:
                os.remove(os.path.join(file_path, name))


def refush_proxy_file(file_path):
    global proxies
    file_path = file_path + '/proxies' + datetime.datetime.today().strftime('%Y-%m-%d') + '.txt'
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf8') as f:
            proxies = f.readlines()
            for i in range(len(proxies)):
                proxies[i] = proxies[i].replace('\n', '')

            f.close()
    else:
        del_proxy_file()
        bath_get_proxies()
        with open(file_path, "a") as f:
            for pro in proxies:
                f.write(pro + '\n')
            f.close()


def bath_get_proxies():  # 随机IP
    agent_url = 'https://www.kuaidaili.com/free/inha/'
    # url = 'https://www.kuaidaili.com/free/'
    proxies_list = []
    for i in range(proxies_num):
        get_proxies(i)
        interval = float(random.randint(1, 30)) / 10
        print('当前页数{},间隔{}秒'.format(str(i), str(interval)))
        time.sleep(interval)


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


def get_random_ip():
    if len(proxies) == 0:
        return None
    proxy_ip = random.choice(proxies)
    proxy = json.loads(proxy_ip)
    return proxy
