import json
import os
import shutil
import sqlite3
import sys
import time
import traceback
from io import BytesIO

import requests
from PIL import Image

from proxiesLoad import refush_proxy_file, get_random_ip

# 易刊配置数据库
catsdown_sqlite_path = 'catsdown.sqlite'
# 易刊虾皮数据库
shopeemy_sqlite_path = 'shopeemy.sqlite'
# 易刊拼多多采集数据库
pdd_sqlite_path = 'yangkeduo.sqlite'

own_sqlite_path = 'owngoods.sqlite'

title_img_path = ''

options_img_dir_name = 'options_img'
des_img_dir_name = 'des_img'
title_img_dir_name = 'title_img'
video_dir_name = 'video'


def load_config():
    global title_img_path, des_img_path, catsdown_sqlite_path, shopeemy_sqlite_path, pdd_sqlite_path
    with open("config.txt", "r", encoding='utf8') as f:
        configList = f.readlines()
        f.close()
    for config in configList:
        config = config.replace('\uFEFF', '')
        if config.startswith('主页图片路径'):
            title_img_path = config.replace('\n', '').split('=')[1]
        if config.startswith('易刊配置数据库'):
            catsdown_sqlite_path = config.replace('\n', '').split('=')[1]
        if config.startswith('易刊虾皮数据库'):
            shopeemy_sqlite_path = config.replace('\n', '').split('=')[1]
        if config.startswith('易刊拼多多采集数据库'):
            pdd_sqlite_path = config.replace('\n', '').split('=')[1]


# 加载分类
def load_classify():
    classify_list = []
    conn = sqlite3.connect(catsdown_sqlite_path)
    c = conn.cursor()
    c.execute('select * from shoppetw')
    rows = c.fetchall()
    for row in rows:
        classify_list.append({'catid': row[1], 'display_name': row[4]})
    c.close()
    conn.close()
    return classify_list


# 加载分组商品信息
def load_shopee_groups(group_name):
    goods_list = []
    conn = sqlite3.connect(shopeemy_sqlite_path)
    c = conn.cursor()
    c.execute("select * from itemview where 分組='{}'".format(group_name))
    rows = c.fetchall()
    for row in rows:
        goods = {'id': row[0],
                 'name': row[1],
                 'price': row[2],
                 'description': row[3],
                 'title_img_items': row[4],
                 'goods_num': row[5],
                 'goods_weight': row[6],
                 'group_name': row[7],
                 'classify_items': row[11],
                 'classify_names': get_classify_names(row[11]),
                 'goodsOptions': row[12],
                 'out_days': row[13],
                 'goods_attribute': row[16],
                 'parcel_size': row[18],
                 'freights': row[19],
                 'website': row[24]
                 }
        goods_list.append(goods)
    c.close()
    conn.close()
    return goods_list


def get_classify_names(classifys):
    classifys_arr = str(classifys).split('-')
    conn = sqlite3.connect(catsdown_sqlite_path)
    c = conn.cursor()
    display_names = []
    for cl in classifys_arr:
        c.execute("select * from shopeetw where catid='{}'".format(cl))
        rows = c.fetchall()
        if len(rows) == 0:
            continue
        display_names.append(rows[0][4])
    c.close()
    conn.close()
    return '#'.join(display_names)


def exists_goods(group_name):
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    c.execute("select * from yikan_infos where group_name='{}'".format(group_name))
    rows = c.fetchall()
    c.close()
    conn.close()
    return len(rows) > 0


def save_goods(group_name):
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    goods_list = load_shopee_groups(group_name)
    total = len(goods_list)
    i = 1
    time_start = time.perf_counter()
    for goods in goods_list:
        pdd_goods = get_goods_info(goods['website'])
        c.execute("""insert into yikan_infos(id,name,price,description,title_img_items,goods_num,
                  goods_weight,group_name,classify_items,classify_names,goodsOptions,out_days,
                  parcel_size,freights,website,des_img_items,video_url,goods_attribute,old_price)
                  values ({},'{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')""".format(
            goods['id'], goods['name'], goods['price'], goods['description'], goods['title_img_items'],
            goods['goods_num'], goods['goods_weight'],
            goods['group_name'], goods['classify_items'], goods['classify_names'], goods['goodsOptions'],
            goods['out_days'], goods['parcel_size'], goods['freights'], goods['website'],

            pdd_goods['des_img_items'], pdd_goods['video_url'], goods['goods_attribute'], pdd_goods['price']
        ))
        progress_bar(i, total, '汇总数据', time_start)
        i = i + 1
    print('\n')
    conn.commit()
    c.close()
    conn.close()


def analyze(img_items, group_name):
    img_json = json.loads(img_items)
    spec_values = img_json[0]['dataRows'][0]['specValue']
    save_path = options_img_dir_name + '\\' + group_name
    if not os.path.exists(options_img_dir_name):
        os.makedirs(options_img_dir_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for spe in spec_values:
        url = spe.get('simage', None)
        if url is None:
            url = spe.get('icon', None)
        if url is None or url == '':
            continue
        save_img(url, save_path)


def progress_bar(curr, total, title, time_start):
    a = "*" * curr
    b = "." * (total - curr)
    c = (curr / total) * 100
    dur = time.perf_counter() - time_start
    print("\r{}进度条：{:^3.0f}%[{}->{}]{:.2f}s".format(title, c, a, b, dur), end="")
    # sys.stdout.flush()


def create_goods_infos():
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    try:
        c.execute('''CREATE TABLE yikan_infos
               (
        id Integer        primary key AUTOINCREMENT,
        name char(255)   not null,-- '名称'
        price char(50) default '', -- '价格',
        description text   default '', -- '描述',
        title_img_items text default '', -- '首页显示图片集合',
        goods_num char(50) default '', -- '商品数量',
        goods_weight char(50) default '', -- '重量',
        group_name char(50)   default '', -- '分组名称',
        classify_items text   default '' ,-- '類別編號',
        classify_names char(255)  default '', -- '类别名称',
        goodsOptions text  default '', -- '商品選項',
        out_days char(50) default '', -- '出货天数',
        parcel_size char(50)  default '', -- '包裹尺寸',
        freights text   default '', --  '運費',
        website char(255)   default '', -- '网址'
        des_img_items  text   default '',-- '描述图片'
        video_url char(255) default '', -- 视频URL
        goods_attribute text default '', -- 商品属性
        old_price char(50) default '' --原本的价格
        );''')
        print("数据表创建成功")
    except:
        print("数据表已存在")
    conn.commit()
    c.close()
    conn.close()


def copy_dirs(src_path, target_path):
    file_count = 0
    source_path = os.path.abspath(src_path)
    target_path = os.path.abspath(target_path)
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    if os.path.exists(source_path):
        time_start = time.perf_counter()
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(root, file)
                shutil.copy(src_file, target_path)
                file_count += 1
                progress_bar(file_count, len(files), '首页图片整理', time_start)

        print('\n')
    return int(file_count)


def get_goods_info(goodswebsite):
    conn = sqlite3.connect(pdd_sqlite_path)
    c = conn.cursor()
    c.execute("select * from itemview where 商品网址='{}'".format(goodswebsite))
    rows = c.fetchall()
    if len(rows) == 0:
        return {'des_img_items': '', 'video_url': '', 'goods_attribute': '', 'price': ''}
    des_arr = str(rows[0][4]).split('<br/>')
    description = []
    title_img_items = []
    for des_item in des_arr:
        if '<img' not in des_item:
            description.append(des_item)
        else:
            temp = des_item.replace('<img src="', '').replace('"/>', '')
            title_img_items.append(temp)
    goods = {'website': rows[0][0],
             'name': rows[0][1],
             'price': rows[0][2],
             'goods_num': rows[0][3],
             'description': ','.join(description),
             'des_img_items': '|'.join(title_img_items),
             'title_img_items': rows[0][6],
             'specification': rows[0][7],
             'shop_number': rows[0][9],
             'goods_number': rows[0][10],
             'goods_attribute': rows[0][12],
             'video_url': rows[0][14],
             }
    c.close()
    conn.close()
    return goods


def save_img(image_url, img_path, target_size=None):
    img_arr = str(image_url).split('/')
    img_name = img_arr[len(img_arr) - 1]
    # 图片URL和目标大小
    # target_size = (750, 750)  # 指定的目标大小

    # 下载并调整图片大小
    resized_image = download_and_resize_image(image_url)
    if resized_image is None:
        return
        # 调整图像大小
    if target_size is not None:
        resized_image = resized_image.resize(target_size, Image.LANCZOS)
    if resized_image:
        # resized_image.show()  # 显示调整后的图片
        resized_image.save(img_path + '\\' + img_name)  # 保存调整后的图片

    # # 图片链接
    # # image_url = "https://www.shuquge.com/files/article/image/3/3478/3478s.jpg"
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    # }
    # try:
    #     r = requests.get(image_url, headers=headers, proxies=get_random_ip())
    # except Exception as e:
    #     print(e)
    #     return
    # # 下载图片
    #
    # # 二进制数据需要用r.content 进行提取
    # # 将图片放在‘图库’文件夹下，‘图库’是文件夹的名称，将图片放入该文件夹中，该文件夹与py文件在同一目录下
    # with open(img_path + '\\' + img_name, 'wb') as f:
    #     f.write(r.content)
    #     f.close()


def download_and_resize_image(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
    }
    try:
        # 发送GET请求以下载图片
        response = requests.get(url, headers=headers, proxies=get_random_ip())
        response.raise_for_status()

        # 将下载的内容转换为Image对象
        img = Image.open(BytesIO(response.content))

        # 调整图像大小
        # img = img.resize(target_size, Image.LANCZOS)

        return img
    except Exception as e:
        print("Error:", e)
        return None


def get_img_items(group_name):
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    c.execute("select* from yikan_infos where group_name='{}'".format(group_name))
    rows = c.fetchall()
    total = len(rows)
    time_start = time.perf_counter()
    for i in range(total):
        analyze(rows[i][10], group_name)
        save_des_img(rows[i][15], group_name)
        save_video(rows[i][16], group_name)
        progress_bar(i + 1, total, '整理影像', time_start)
    print('\n')


def save_video(video_url, group_name):
    save_path = video_dir_name + '\\' + group_name
    if not os.path.exists(video_dir_name):
        os.makedirs(video_dir_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    if video_url is None or video_url == '':
        return
    save_img(video_url, save_path)


def save_des_img(img_urls, group_name):
    img_url_arr = str(img_urls).split('|')
    save_path = des_img_dir_name + '\\' + group_name
    if not os.path.exists(des_img_dir_name):
        os.makedirs(des_img_dir_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    for url in img_url_arr:
        if url is None or url == '':
            continue
        save_img(url, save_path, target_size=(750, 750))


def del_data(group_name):
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    row_count = c.execute("delete from yikan_infos where group_name='{}'".format(group_name))
    conn.commit()
    c.close()
    conn.close()
    return row_count


def del_img(group_name):
    des_save_path = des_img_dir_name + '\\' + group_name
    options_save_path = options_img_dir_name + '\\' + group_name
    title_save_path = title_img_dir_name + '\\' + group_name
    if os.path.exists(des_save_path):
        shutil.rmtree(des_save_path)
    if os.path.exists(options_save_path):
        shutil.rmtree(options_save_path)
    if os.path.exists(title_save_path):
        shutil.rmtree(title_save_path)


def input_group_name():
    group_name = input('输入分组名称：')
    if exists_goods(group_name):
        result = input('当前分组[{}]已存在，是否删除Y/N?'.format(group_name))
        if result.lower() == 'y':
            del_data(group_name)
            del_img(group_name)
        else:
            input_group_name()
    return group_name


def _main_():
    try:
        refush_proxy_file(__file__)
        load_config()
        create_goods_infos()
        group_name = input_group_name()
        save_goods(group_name)
        get_img_items(group_name)
        copy_dirs(title_img_path + '\\' + group_name, 'title_img\\' + group_name)
        print('分组数据同步成功')
    except:
        traceback.print_exc()
    input('回车键退出')
    sys.exit()


if __name__ == '__main__':
    _main_()
