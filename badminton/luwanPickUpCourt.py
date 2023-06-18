import datetime
import json
import os
import random
import sys
import time
import traceback

import psutil
import schedule
import win32gui
import win32con

import requests

proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888"}
verify_str = "FiddlerRoot.pem"
token_file_path = r'D:\private\51yundong.txt'
court_url = 'https://mapv2.51yundong.me/api/stadium/resources/2c93809e821eb0ed018229e727b900af/matrix?stadiumItemId={}&date={}'
submit_url = 'https://mapv2.51yundong.me/api/order/orders?orderType=1'
notice_url = 'http://www.pushplus.plus/send?token=7cb7768ebc2b41a4b4ca047ccdc621a1&title={}&content={}&template=html'
stadiumItemId = '2c93809e821eb0ed018229e727b900af'
stadiumId = '2c93809e821eb0ed018229e727b600ae'
headers = {
    "Content-Type": "application/json"
}
court_all_list = [
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611304093470722', 'fieldName': '一号场（单）', 'fieldNo': 1, 'periodDate': '2023-02-08',
     'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611356115423233', 'fieldName': '二号场', 'fieldNo': 2, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611387094552578', 'fieldName': '三号场', 'fieldNo': 3, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611419185172481', 'fieldName': '四号场', 'fieldNo': 4, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611457810518018', 'fieldName': '五号场', 'fieldNo': 5, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611503041892353', 'fieldName': '六号场', 'fieldNo': 6, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611537552625666', 'fieldName': '七号场', 'fieldNo': 7, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611779849179137', 'fieldName': '八号场', 'fieldNo': 8, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611815538511873', 'fieldName': '九号场（单）', 'fieldNo': 9, 'periodDate': '2023-02-08',
     'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611859796807682', 'fieldName': '十号场', 'fieldNo': 10, 'periodDate': '2023-02-08', 'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08',
     'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08',
     'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08',
     'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08',
     'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611900867432449', 'fieldName': '十一号场', 'fieldNo': 11, 'periodDate': '2023-02-08',
     'start': 1260,
     'time': 21.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 540,
     'time': 9.0, 'price': 2000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 600,
     'time': 10.0, 'price': 2000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 660,
     'time': 11.0, 'price': 2000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 720,
     'time': 12.0, 'price': 2000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 780,
     'time': 13.0, 'price': 2000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 840,
     'time': 14.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 900,
     'time': 15.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08', 'start': 960,
     'time': 16.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08',
     'start': 1020,
     'time': 17.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08',
     'start': 1080,
     'time': 18.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08',
     'start': 1140,
     'time': 19.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08',
     'start': 1200,
     'time': 20.0, 'price': 6000},
    {'fieldId': '1540611939924791298', 'fieldName': '十二号场', 'fieldNo': 12, 'periodDate': '2023-02-08',
     'start': 1260,
     'time': 21.0, 'price': 6000}

]
req = requests.session()
info_list = []
task_is_run = True
start = 0
logged = False
fiddler_is_start = False
start_diff = '1'
next_run_time = datetime.datetime.now()


def _main_():
    global info_list, start_diff
    exec_time = '00:00'
    with open("51yundong.txt", "r", encoding='utf8') as f:
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
        if config.startswith('时间段'):
            times_str = config.replace('\n', '').split('=')[1]
            if times_str != '':
                times = times_str.split(',')
        if config.startswith('启动时差'):
            start_diff = config.replace('\n', '').split('=')[1]
    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')

    for time_s in times:
        info_list.append({'resourceDate': init_date, 'fieldNo': field_no, 'time': float(time_s)})
    # info_list = [{'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[0])},
    #              {'resourceDate': init_date, 'fieldNo': field_no, 'time': float(times[1])}]
    # fiddler_start()
    close_win_class()
    # login()
    # task()
    schedule_task(exec_time)


def close_win_class():
    hwnd = win32gui.FindWindow("Chrome_WidgetWin_0", "来沪动丨健身地图")  # 获取窗口
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
    time.sleep(0.1)


def task():
    global task_is_run
    task_is_run = True
    # current_random = float(random.randint(1 * 1000, 2 * 1000)) / 1000
    # print('延迟{}秒'.format(current_random))
    # time.sleep(current_random)

    init_date = datetime.datetime.strftime(datetime.datetime.today() + datetime.timedelta(days=1), '%Y-%m-%d')
    for info in info_list:
        info['resourceDate'] = init_date
    # info_list[0]['resourceDate'] = init_date
    # info_list[1]['resourceDate'] = init_date
    while True:
        try:
            result_list = get_court()
            court_no_first = 0
            court_no_second = 0
            num = int(info_list[0]['fieldNo'])
            temp_first = 0
            temp_second = 0
            for item in result_list:
                if item['fieldNo'] == 1 or item['fieldNo'] == 9:
                    continue
                if num == 0:
                    break
                if int(info_list[0]['time']) == int(item['time']):
                    court_no_first = item['fieldNo']
                if int(info_list[1]['time']) == int(item['time']):
                    court_no_second = item['fieldNo']
                if court_no_first == court_no_second and court_no_first != 0:
                    temp_first = court_no_first
                    temp_second = court_no_second
                    court_no_first = 0
                    court_no_second = 0
                    num = num - 1
            if (court_no_first == 0 or court_no_second == 0) and (temp_first == 0 or temp_second == 0):
                print('{}没有{}时间段场地'.format(info_list[0]['resourceDate'],
                                                  str(int(info_list[0]['time'])) + '、' + str(
                                                      int(info_list[1]['time']))))
            else:
                if court_no_first == 0 or court_no_second == 0:
                    court_no_first = temp_first
                    court_no_second = temp_second
                info_list[0]['fieldNo'] = court_no_first
                info_list[1]['fieldNo'] = court_no_second
                pickup_court()

            break
        except:
            traceback.print_exc()
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
                    "stadiumSource": stadiumSource, "channel": 1, "orderType": "1"}
    for item in info_list:
        fieldId = None
        fieldName = None
        price = None
        for param in court_all_list:
            if param['fieldNo'] == item['fieldNo'] and param['time'] == item['time']:
                fieldId = param['fieldId']
                fieldName = param['fieldName']
                price = param['price']
                break
        if fieldId is None:
            continue
        detail = {"beginTime": str(int(item['time'])) + ':00', "endTime": str(int(item['time']) + 1) + ':00',
                  "fieldId": fieldId,
                  "fieldName": fieldName, "resourceDate": item['resourceDate'], "amount": price,
                  "sessionId": item['resourceDate']}
        submit_param['details'].append(detail)
    submit_start = time.perf_counter()
    result_response = req.post(submit_url, json=submit_param, headers=headers, verify=verify_str, proxies=proxies)
    result_json = json.loads(result_response.content)
    print(result_json)
    if result_json['code'] == 200:
        requests.get(notice_url.format('卢湾{}场地预订成功'.format(info_list[0]['fieldNo']), info_list))
    else:
        print('卢湾{}场地预订失败'.format(info_list[0]['fieldNo']))
    end = time.perf_counter()
    print('提交耗时：{:.4f}s'.format(end - submit_start))
    print('下订单成功总耗时：{:.4f}s'.format(end - start))
    print('当前时间：{}'.format(datetime.datetime.now()))


def get_court():
    global start
    start = time.perf_counter()
    temp_url = court_url.format(stadiumItemId, info_list[0]['resourceDate'])
    result_response = req.get(temp_url, headers=headers, verify=verify_str, proxies=proxies)
    end = time.perf_counter()
    print('加载场地数据耗时：{:.4f}s'.format(end - start))
    result_json = json.loads(result_response.content)
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
        print('{}18点以后的场地无'.format(info_list[0]['resourceDate']))
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
        w.write(curr_date_str+' '+token + '\n')
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
            if next_run_time > datetime.datetime.now():
                return None
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
        if 300 > diff_seconds > 0 and fiddler_is_start is False:
            fiddler_start()
        if 0 < diff_seconds < 30:
            interval = 0.01
        if float(start_diff) >= diff_seconds > 0 and logged is False:
            login()
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


if __name__ == '__main__':
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
