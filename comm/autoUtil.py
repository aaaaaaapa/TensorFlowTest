import time
from ctypes import windll

import pyautogui
import win32con
import win32gui

u = windll.LoadLibrary('user32.dll')


def active_window(title, name):
    result = u.GetForegroundWindow()
    if result == 0 or result == 67622:
        print('锁屏状态不能推送消息')
        return
    # windll.user32.BlockInput(1)
    hwnd = win32gui.FindWindow(title, name)  # 获取窗口
    if hwnd == 0:
        print('窗口未打开')
        return
    if win32gui.IsWindowVisible(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    if win32gui.IsIconic(hwnd) == 0:
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
    win32gui.SetForegroundWindow(hwnd)
    curr = win32gui.GetWindowRect(hwnd)
    return curr


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
