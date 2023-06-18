import requests
from PIL import Image
from fake_useragent import UserAgent
from matplotlib import pyplot as plt

from showImg import show_img
import os
import random
import shutil
import sys
import time


def get_random_ua():  # 随机UA
    ua = UserAgent()
    return ua.random


# def show_img():
#     png = Image.open('img/123.png')
#     plt.figure('123')
#     plt.imshow(png)
#     print("显示")
#     plt.show()


headers = {
    'User-Agent': get_random_ua()
}
i = 0
if not os.path.exists('img'):
    os.mkdir('img')
while True:
    codeUrl = "https://jywg.18.cn/Login/YZM?randNum={}".format(str(random.random()))
    # 获取验证码图片，并保存下来为123.png
    response = requests.get(codeUrl, headers=headers)
    img = response.content
    with open('img/123.png', 'wb') as f:
        f.write(img)
        f.close

    show_img('img/123.png')
    cap = input("验证码：")

    if cap == '':
        continue
    if cap == 'exit':
        break
    if not os.path.exists('img/' + cap):
        os.mkdir('img/' + cap)
    shutil.move('img/123.png', 'img/{}/{}.png'.format(cap, str(int(time.time()))))
    i = i + 1
    print('校验数量；{}'.format(str(i)))
sys.exit()
