import base64
import codecs
import sys
import time
from ctypes import windll

import chardet as chardet
import pyautogui
import win32com.client
import cv2
import numpy as np
import win32con
import win32gui

from PIL import Image

from ddddocr import DdddOcr


def get_postion(chunk, canves):
    """
    判断缺口位置
    :param chunk: 缺口图片是原图
    :param canves:
    :return: 位置 x, y
    """
    otemp = chunk
    oblk = canves
    target = cv2.imread(otemp, 0)
    template = cv2.imread(oblk, 0)
    # w, h = target.shape[::-1]
    temp = 'temp.jpg'
    targ = 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    return x, y


def identify_gap(bg, tp, out):
    '''
    bg: 背景图片
    tp: 缺口图片
    out:输出图片
    '''
    # 读取背景图片和缺口图片
    bg_img = cv2.imread(bg)  # 背景图片
    tp_img = cv2.imread(tp)  # 缺口图片

    # 识别图片边缘
    bg_edge = cv2.Canny(bg_img, 100, 200)
    tp_edge = cv2.Canny(tp_img, 100, 200)

    # 转换图片格式
    bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2RGB)
    tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2RGB)

    # 缺口匹配
    res = cv2.matchTemplate(bg_pic, tp_pic, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)  # 寻找最优匹配

    # 绘制方框
    th, tw = tp_pic.shape[:2]
    tl = max_loc  # 左上角点的坐标
    br = (tl[0] + tw, tl[1] + th)  # 右下角点的坐标
    cv2.rectangle(bg_img, tl, br, (0, 0, 255), 2)  # 绘制矩形
    cv2.imwrite(out, bg_img)  # 保存在本地

    # 返回缺口的X坐标
    return tl[0]


def find_img(img, clicks):
    image_l = pyautogui.locateOnScreen(img, grayscale=True)
    center = pyautogui.center(image_l)
    return center
    # pyautogui.click(center, interval=0.1, clicks=clicks, duration=0.1)


def click_move(xOffset, yOffset):
    pyautogui.dragRel(xOffset, yOffset, duration=0.5, button='right')


def _main():
    try_num = 0
    det = DdddOcr(det=False, ocr=False)
    u = windll.LoadLibrary('user32.dll')
    while True:
        result = u.GetForegroundWindow()
        if result == 0 or result == 67622:
            print('锁屏状态不能推送消息')
            pyautogui.press('enter')
            time.sleep(0.5)
            pyautogui.typewrite('2651')
            time.sleep(0.5)
        # windll.user32.BlockInput(1)
        hwnd = win32gui.FindWindow("Chrome_WidgetWin_0", "久事体育场馆")  # 获取窗口
        if win32gui.IsWindowVisible(hwnd) == 0:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        if win32gui.IsIconic(hwnd) == 0:
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
        win32gui.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        image_l = pyautogui.locateOnScreen('..\\img\\5.png', grayscale=True)
        if image_l is None:
            break
        with open('D:\private\customRules_log.txt', "r", encoding='utf-16le') as f:
            imageDataL = f.readline().replace('\ufeff', '').replace('\n', '')
            ImageDataS = f.readline().replace('\ufeff', '').replace('\n', '')

        target_bytes = base64.b64decode(imageDataL)
        background_bytes = base64.b64decode(ImageDataS)
        # bg_img = '../img/L_4.png'
        # slider_img = '../img/S_4.png'
        #
        #
        # with open(slider_img, 'rb') as f:
        #     target_bytes = f.read()
        #
        # with open(bg_img, 'rb') as f:
        #     background_bytes = f.read()
        diff = 0
        res = det.slide_match(target_bytes, background_bytes, simple_target=True)
        time.sleep(0.1)
        image_l = pyautogui.locateOnScreen('..\\img\\slider.png', grayscale=True)
        center = pyautogui.center(image_l)
        pyautogui.moveTo(center, duration=0)
        # square_x = (res['target'][2] - res['target'][0])
        length = (res['target'][0]) / 2 - diff
        pyautogui.dragRel(length, 0, duration=0.5, button='left')
        # print(res)
        try_num = try_num + 1
        time.sleep(0.3)
    print_str = '滑块验证成功尝试次数：{}'.format(try_num)
    print(print_str)
    with open('..\\log\\try_log.txt', 'ab') as f:
        f.writelines(print_str)


if __name__ == '__main__':
    _main()

    sys.exit()
