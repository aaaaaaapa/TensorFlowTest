import base64
import json
import os
import re
import sqlite3
import sys
import time
import traceback

import opencc
from PIL import Image
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from six import BytesIO

from ddddocr import DdddOcr
from shopee.shopeeTideUp import own_sqlite_path, title_img_dir_name, des_img_dir_name, video_dir_name, \
    options_img_dir_name

ocr = DdddOcr()
service = Service(r'D:\private\chromedriver\chromedriver.exe')
# service = Service(r'D:\private\msedgedriver\msedgedriver.exe')

driver = ''

url = 'https://seller.shopee.tw/'
cookies_List = []
title_img_list = [r'C:\Users\yanfeng\Desktop\商品\1.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\2.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\3.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\4.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\5.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\6.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\7.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\8.jpg',
                  r'C:\Users\yanfeng\Desktop\商品\9.jpg']

title_video = r'C:\Users\yanfeng\Desktop\商品\1.mp4'

description_str = """____________暖暖____________

 親愛的買家，

 由於7-11有相關超材重量限制 (材積：需 ≦ 45cm*30cm*30cm，最長邊 ≦ 45cm，其他兩邊則需均 ≦ 30cm；重量不得超過10公斤)
 故選擇超商取件，超過尺寸的話，建議選擇"蝦皮宅配"物流方式哦，以避免因超材超重無法配送而取消訂單。

?㊣新店開張！陸續上新品中！優質生活 從這裡開始

??全店不滿159元不出貨哦??

每天下午5點前截單，除非有質量問題，不然都會當天發貨。
?本店所有產品均從源頭廠家拿貨 ，免去中間商賺差價，價格優惠， 質量放心 。 能下單的都是有現貨哦， 請放心下單吧 。
（店里所有產品都可以下單備注款式哦， 店主看到后會幫您發出您想要的款哦） 一般5-7天即可到臺灣，早下單就可以早收到哦 全店大量的 優惠， 同時您還可以領取優惠券，
?買的越多 省的越多 有任何疑問請聯系客戶哦 。 （客服上班時間8:30-22:00 ）"""

class_attribute_List = [{"n": "品牌", "vn": "自有/其他品牌", "v": "0", "k": "brand_id", "m": False},
                        {"n": "泳裝類型", "vn": "運動泳裝", "k": "100942", "m": False},
                        {"n": "尺寸（長 x 寬 x 高）", "vn": "", "k": "100942", "m": False},
                        {"n": "保固期限", "vn": "", "k": "100121", "m": False},
                        {"n": "保固種類", "vn": "", "k": "100370", "m": False},
                        {"n": "組裝", "vn": "", "k": "100730", "m": False},
                        {"n": "古董收藏", "vn": "", "k": "100729", "m": False},
                        {"n": "材質", "vn": "", "k": "100134", "m": False},
                        {"n": "產地", "vn": "", "k": "100037", "m": False},
                        {"n": "可承重量", "vn": "", "k": "100828", "m": False},
                        {"n": "包裝尺寸", "vn": "", "k": "101029", "m": False},
                        {"n": "每組數量", "vn": "", "k": "100999", "m": False}]

googds_infos = [{
    "dataRows": [{
        "name": "型號（背框顔色免費客制）",
        "specValue": [{
            "name": "【黑色】+軟質升降扶手+靠背可躺",
            "simage": "https://s-cf-sg.shopeesz.com/file/d807f7e8e2804251fab15d11768ca889"
        }, {
            "name": "【典雅灰】軟質升降扶手+靠背可躺",
            "simage": "https://s-cf-sg.shopeesz.com/file/667110276b2cb8055c63983582fdce34"
        }]
    }, {
        "name": "規格（背框顔色免費客制）",
        "specValue": [{
            "name": "伸縮腳墊+金屬腿盤+靜音輪+全網坐墊"
        }, {
            "name": "電鍍金屬腿盤+靜音輪+海綿坐墊"
        }, {
            "name": "尼龍腿盤+靜音輪+全網紋坐墊"
        }, {
            "name": "電鍍金屬腿盤+靜音輪+全網紋坐墊"
        }, {
            "name": "尼龍腿盤+靜音輪+海綿坐墊"
        }]
    }]
}, {
    "【黑色】+軟質升降扶手+靠背可躺/伸縮腳墊+金屬腿盤+靜音輪+全網坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4780",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [0, 4],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 183586416525,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【典雅灰】軟質升降扶手+靠背可躺/電鍍金屬腿盤+靜音輪+海綿坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "3980",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [1, 1],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 163298887817,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【黑色】+軟質升降扶手+靠背可躺/尼龍腿盤+靜音輪+全網紋坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4168",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [0, 2],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 181042340608,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【典雅灰】軟質升降扶手+靠背可躺/尼龍腿盤+靜音輪+全網紋坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4380",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [1, 2],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 181042340609,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【黑色】+軟質升降扶手+靠背可躺/電鍍金屬腿盤+靜音輪+海綿坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "3780",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [0, 1],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 163298887821,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【黑色】+軟質升降扶手+靠背可躺/電鍍金屬腿盤+靜音輪+全網紋坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4268",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [0, 3],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 181042340613,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【典雅灰】軟質升降扶手+靠背可躺/尼龍腿盤+靜音輪+海綿坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "3880",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [1, 0],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 163298887816,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【黑色】+軟質升降扶手+靠背可躺/尼龍腿盤+靜音輪+海綿坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "3680",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [0, 0],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 163298887820,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【典雅灰】軟質升降扶手+靠背可躺/電鍍金屬腿盤+靜音輪+全網紋坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4480",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [1, 3],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 181042340611,
        "originalQty": 10,
        "has_gimmick_tag": False
    },
    "【典雅灰】軟質升降扶手+靠背可躺/伸縮腳墊+金屬腿盤+靜音輪+全網坐墊": {
        "itemid": 20312755314,
        "status": 1,
        "current_promotion_reserved_stock": 0,
        "promotionid": 0,
        "price": "4980",
        "price_stocks": [{
            "allocated_stock": 0,
            "stock_breakdown_by_location": None
        }],
        "current_promotion_has_reserve_stock": False,
        "normal_stock": 10,
        "extinfo": {
            "tier_index": [1, 4],
            "group_buy_info": None,
            "is_pre_order": True,
            "estimated_days": 15
        },
        "price_before_discount": 0,
        "modelid": 183586416526,
        "originalQty": 10,
        "has_gimmick_tag": False
    }
}]
path_prefix = os.path.dirname(__file__)
path_prefix = os.path.dirname(__file__)


def button_verify(button_sure):
    elem_type_sure = get_element(button_sure, 'button')
    if elem_type_sure.is_enabled():
        elem_type_sure.click()
        return True
    return False


def get_element(text, ele_type, ele_class=None, attempt=20):
    class_name = ''
    if ele_class is not None:
        class_name = "[@class='{}']".format(ele_class)
    for i in range(attempt):
        elements = driver.find_elements(By.XPATH, "//{}{}".format(ele_type, class_name))
        for element in elements:
            if element.text == text:
                return element
        time.sleep(1)
    return None


def select_other(element):
    if element is None:
        get_element('其他', 'p')
    return element


def get_item(item_name, xpath):
    type_items = driver.find_elements(By.XPATH, xpath)
    for item in type_items:
        if item_name in item.text:
            scroll_to(item)
            return item
    return None


def verify_load(num=30):
    for i in range(num):
        try:
            driver.find_element(By.XPATH, '//input[@accept="image/*"]')
        except:
            time.sleep(1)
            continue
        return


def load_goods_by_group(group_name):
    work_infos = []
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    c.execute("select * from yikan_infos where group_name='{}' and islisting='0'".format(group_name))
    rows = c.fetchall()
    for row in rows:
        info = {'id': row[0], 'name': row[1], 'price': row[2], 'description': row[3],
                'title_img_items': get_title_img_items(row[4], group_name), 'goods_num': row[5], 'goods_weight': row[6],
                'group_name': row[7], 'classify_items': row[8], 'classify_names': row[9],
                'goodsOptions': get_goods_options_items(row[10], group_name), 'out_days': row[11],
                'parcel_size': row[12],
                'freights': row[13], 'website': row[14], 'des_img_items': get_des_img_items(row[15], group_name),
                'video_url': get_video_name(row[16], group_name),
                'goods_attribute': row[17], 'old_price': row[18]}
        work_infos.append(info)
    c.close()
    conn.close()
    return work_infos


def get_title_img_items(img_items_Str, group_name):
    title_img_items = []
    title_img_temps = str(img_items_Str).split('|')
    path = path_prefix + '\\' + title_img_dir_name + '\\' + group_name
    for temp in title_img_temps:
        paths = temp.split('\\')
        file_name = paths[len(paths) - 1]
        file_name = file_name.replace(group_name, '')
        if '_' in file_name:
            temp_names = file_name.split('_')
            file_name = temp_names[0] + '.jpg'
        title_img_items.append(path + '\\' + file_name)
    return title_img_items


def get_des_img_items(img_items_Str, group_name):
    des_img_items = []
    urls = str(img_items_Str).split('|')
    path = path_prefix + '\\' + des_img_dir_name + '\\' + group_name
    for img_url in urls:
        temps = img_url.split('/')
        img_name = temps[len(temps) - 1]
        des_img_items.append(path + '\\' + img_name)
    return des_img_items


def get_video_name(video_url, group_name):
    temps = str(video_url).split('/')
    video_name = temps[len(temps) - 1]
    if video_name == '':
        return ''
    return path_prefix + '\\' + video_dir_name + '\\' + group_name + '\\' + video_name


def get_goods_options_items(goods_options, group_name):
    goods_options_items = []
    img_json = json.loads(goods_options)
    spec_values = img_json[0]['dataRows'][0]['specValue']
    path = path_prefix + '\\' + options_img_dir_name + '\\' + group_name
    for i in range(len(spec_values)):
        name = spec_values[i]['name']
        url = spec_values[i].get('simage', None)
        if url is None:
            url = spec_values[i].get('icon', None)
        temps = str(url).split('/')
        img_name = path + '\\' + temps[len(temps) - 1]
        info = {'name': name, 'url': url, 'img_name': img_name}
        goods_options_items.append(info)
        img_json[0]['dataRows'][0]['specValue'][i]['simage'] = img_name
    return img_json


# 上架后修改商品状态
def update_yikan_infos(id):
    conn = sqlite3.connect(own_sqlite_path)
    c = conn.cursor()
    c.execute("update yikan_infos set islisting='1'  where  id={}".format(id))
    conn.commit()
    c.close()
    conn.close()


def find_element(xpath, max_num=20, driver_item=None):
    index = 0
    if driver_item is None:
        driver_item = driver
    while index < max_num:
        try:
            elements = driver_item.find_elements(By.XPATH, xpath)
            if len(elements) == 1:
                scroll_to(elements[0])
                return elements[0]
            else:
                time.sleep(1)
        except:
            traceback.print_exc()
            time.sleep(1)
        index = index + 1
    return None


def scroll_to(element):
    result = element.location
    x = result['x']
    y = result['y'] - 200
    if y < 0:
        y = 0
    js = "window.scrollTo({},{})".format(0, y)
    driver.execute_script(js)
    time.sleep(1)


def element_click(element):
    try:
        element.click()
    except:
        traceback.print_exc()
        time.sleep(1)


def exec_listing(work_info):
    driver.get('https://seller.shopee.tw/portal/product/new')
    # set_navigator()
    verify_load(500)
    for img in work_info['title_img_items']:
        elem_upload_input = find_element('//input[@accept="image/*"]')
        if os.path.exists(img):
            elem_upload_input.send_keys(img)
        time.sleep(1)
    elem_upload_input = find_element('//input[@accept="video/mp4"]')
    # 视频
    if work_info['video_url'] != '':
        elem_upload_input.send_keys(work_info['video_url'])
        time.sleep(3)
        button_verify('確認')
    element_input = find_element('//input[@placeholder="請輸入"]')
    # cc = opencc.OpenCC('s2t')
    # goods_name = cc.convert(goods_name)
    # 商品名称
    element_input.send_keys(work_info['name'])
    elem_goods_type = find_element("//span[contains(text(), '請選擇商品分類')]/..")
    # 分类
    goods_types = str(work_info['classify_names']).split('#')

    elem_goods_type.click()
    time.sleep(1)
    type_first = goods_types[0]
    elem_type_first = get_element(type_first, 'p')
    elem_type_first.click()
    time.sleep(1)
    type_two = goods_types[1]

    elem_type_two = get_element(type_two, 'p')
    elem_type_two = select_other(elem_type_two)
    elem_type_two.click()
    time.sleep(1)
    if button_verify('確認') is False:
        type_three = goods_types[2]
        elem_type_three = get_element(type_three, 'p')
        elem_type_three = select_other(elem_type_three)
        elem_type_three.click()
        time.sleep(2)
        if button_verify('確認') is False:
            type_four = goods_types[3]
            elem_type_four = get_element(type_four, 'p')
            elem_type_four = select_other(elem_type_four)
            elem_type_four.click()
            time.sleep(1)
            button_verify('確認')
    time.sleep(3)
    elem_type_sure = find_element("//div[@data-placeholder='{}']".format('請輸入商品描述或點選以新增圖片'), max_num=100)
    # 描述
    elem_type_sure.send_keys(work_info['description'])
    # elem_description_img = driver.find_element(By.XPATH, "//input[@accept='image/jpg,image/jpeg,image/png']")
    # # 描述图片
    # for item in work_info['des_img_items']:
    #     elem_description_img.send_keys(item)
    #     time.sleep(3)

    time.sleep(1)
    driver.execute_script("document.documentElement.scrollTop=1000")
    time.sleep(1)
    attribute_list = json.loads(work_info['goods_attribute'])
    for attribute in attribute_list:
        if attribute['vn'] != '':
            item_ele = get_item(attribute['n'], "//div[@class='attribute-select-item']")
            item_ele.click()
            time.sleep(1)
            find_element("//div[contains(text(), '{}')]".format(attribute['vn']), driver_item=item_ele).click()
            time.sleep(1)
        # item_ele.send_keys(attribute['vn'])
    driver.execute_script("document.documentElement.scrollTop=1500")
    time.sleep(1)
    find_element("//span[contains(text(),'開啟商品規格')]/..").click()
    time.sleep(1)

    row = work_info['goodsOptions'][0]['dataRows'][0]
    spec_name = row['name']  # 型号
    spec_ele = find_element("//input[@placeholder='{}']".format('例如：顏色'))
    spec_ele.send_keys(spec_name)
    time.sleep(1)
    simage_list = []
    spec_num = 0
    spec_values = row['specValue']
    for spec_value in spec_values:
        value_eles = driver.find_elements(By.XPATH, "//input[@placeholder='{}']".format('例如：紅色，白色'))
        spec_value_name = spec_value['name']
        spec_value_simage = spec_value['simage']
        simage_list.append(spec_value_simage)
        value_eles[spec_num].send_keys(spec_value_name)
        time.sleep(1.5)
        spec_num = spec_num + 1
    element = find_element("//span[contains(text(),'新增規格')]/..")
    element.click()
    time.sleep(1)
    row = work_info['goodsOptions'][0]['dataRows'][1]
    spec_name = row['name']  # 型号
    spec_ele = find_element("//input[@placeholder='{}']".format('例如：尺寸'))
    spec_ele.send_keys(spec_name)
    time.sleep(1)
    spec_num = 0
    spec_values = row['specValue']
    for spec_value in spec_values:
        value_eles = driver.find_elements(By.XPATH, "//input[@placeholder='{}']".format('例如：S, M'))
        spec_value_name = spec_value['name']
        # spec_value_simage = spec_value['simage']
        value_eles[spec_num].send_keys(spec_value_name)
        time.sleep(1)
        spec_num = spec_num + 1
    image_eles = driver.find_elements(By.XPATH, "//input[@accept='image/*']")
    for i in range(1, len(image_eles)):
        image_eles[i].send_keys(simage_list[i - 1])
        time.sleep(1)

    options_elements = driver.find_elements(By.XPATH, "//input[@isround='true'][@placeholder='請輸入']")
    data_list = [options_elements[i:i + 3] for i in range(0, len(options_elements) - 1, 3)]
    num = 0
    options_list = list(work_info['goodsOptions'][1].values())
    for price_ele, num_ele, none_ele in data_list:
        info = options_list[num]
        price_ele.send_keys(info['price'])
        time.sleep(0.5)
        num_ele.send_keys(info['originalQty'])
        time.sleep(0.5)
        num = num + 1
    options_elements[len(options_elements) - 1].send_keys(0.2)
    time.sleep(1)
    wide_ele = find_element("//input[@isround='true'][@placeholder='寬']")
    wide_ele.send_keys(2)
    time.sleep(1)
    length_ele = find_element("//input[@isround='true'][@placeholder='長']")
    length_ele.send_keys(2)
    time.sleep(1)
    height_ele = find_element("//input[@isround='true'][@placeholder='高']")
    height_ele.send_keys(2)
    time.sleep(1)
    driver.execute_script("document.documentElement.scrollTop=10000")
    time.sleep(1)
    while True:
        swith_elements = driver.find_elements(By.XPATH,
                                              "//div[@class='shopee-switch shopee-switch--close shopee-switch--normal']//..")
        if len(swith_elements) == 0:
            break
        else:
            element_click(swith_elements[0])
        time.sleep(2)
    time.sleep(2)
    driver.find_elements(By.XPATH, "//label[@class='shopee-radio']")[1].click()
    time.sleep(1)
    inventory_elements = driver.find_elements(By.XPATH, "//input[@placeholder='0']")
    if len(inventory_elements) == 1:
        inventory_elements[0].clear()
        inventory_elements[0].send_keys(7)
    elem_description_img = find_element("//input[@accept='image/jpg,image/jpeg,image/png']")
    # 描述图片
    for item in work_info['des_img_items']:
        elem_description_img.send_keys(item)
        time.sleep(3)
    button_verify('儲存並下架')
    time.sleep(10)
    update_yikan_infos(work_info['id'])


def load_cookies():
    global cookies_List
    with open("cookies.txt", "r", encoding='utf8') as f:
        cookies_str = f.read()
        f.close()
    cookies_List = json.loads(cookies_str)
    for i in range(len(cookies_List)):
        for key in cookies_List[i].keys():
            if cookies_List[i][key] is None:
                cookies_List[i][key] = 'None'


def set_navigator():
    script = 'Object.defineProperty(navigator,"webdriver",{get:() => false,});'
    # 运行Javascript
    driver.execute_script(script)


def _main_():
    global driver
    load_cookies()
    group_name = input('输入分组名称：')
    work_infos = load_goods_by_group(group_name)
    # chrome_options = Options()
    # chrome_options.page_load_strategy = 'none'  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    # set_navigator()
    for cookies in cookies_List:
        driver.add_cookie(cookie_dict=cookies)
    # 账号填充输入

    for work_info in work_infos:
        exec_listing(work_info)
    driver.quit()
    service.stop()
    time.sleep(0.1)
    # os.system(r'start "" /d "C:\Program Files (x86)\Notepad++" /wait "notepad++.exe" "./log/20220824.txt"')
    # win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Notepad++\notepad++.exe', path, '', 1)
    sys.exit()


if __name__ == '__main__':
    try:

        _main_()


    except Exception as ex:
        traceback.print_exc()
        driver.quit()
        service.stop()
        sys.exit()
