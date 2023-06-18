import sys
import threading
import time
import tkinter as tk
from tkinter import messagebox

import requests

import securitiesSub as stk
import db.stockSub as stkdb
import comm.commPub as com
import asyncio

req = requests.session()
user_id_list = stkdb.query_db()
root = tk.Tk()


def exit_application():
    if messagebox.askyesno("Exit", "Do you really want to quit?"):
        root.destroy()
        sys.exit()


def stock_task(select):
    # stk.exec_task(req, select, user_id_list)
    # threading.Thread(target=get_delay_data).start()
    com.luck_list.clear()
    stk.exec_task(req, select, user_id_list)
    get_delay_data()


def get_delay_data():
    for i in range(100):
        if len(com.luck_list) > 0:
            root.children['frame'].children['label_print'].config(text='\n'.join(com.luck_list))
            break
        time.sleep(0.1)


root.title("My Application")

# 菜单
menubar = tk.Menu(root)
stockMenu = tk.Menu(menubar, tearoff=0)
stockMenu.add_command(label='打新债', command=lambda: stock_task(1))
stockMenu.add_command(label='查询中签', command=lambda: stock_task(2))
stockMenu.add_command(label='查询收益', command=lambda: stock_task(3))
stockMenu.add_command(label='查询申购结果', command=lambda: stock_task(4))
stockMenu.add_command(label='自动打新债', command=lambda: stock_task(5))
stockMenu.add_command(label='查询持仓', command=lambda: stock_task(6))
stockMenu.add_command(label='可转债缴款', command=lambda: stock_task(7))
stockMenu.add_command(label='查询余额', command=lambda: stock_task(8))
stockMenu.add_command(label='卖出转债', command=lambda: stock_task(9))
stockMenu.add_command(label='可转债放弃查询', command=lambda: stock_task(10))
# stockMenu.add_separator()
# 0、退出；1、打新债；2、查询中签；3、查询收益；4、查询申购结果；5、自动打新债；6、查询持仓；7、可转债缴款；8、查询余额；9、卖出转债；10、可转债放弃查询
menubar.add_cascade(label='证券', menu=stockMenu)
root.config(menu=menubar)

# 容器
frame = tk.Frame(root, name='frame', width=300, height=200)
frame.pack()

label = tk.Label(frame, text='这是个标签', name='label_print')
label.pack(pady=10)

root.mainloop()
