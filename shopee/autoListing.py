import base64
import os
import re
import sys
import time
import traceback
import opencc
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from six import BytesIO

from ddddocr import DdddOcr
import sqlite3

# conn = sqlite3.connect('test.db')

ocr = DdddOcr()
service = Service(r'C:\Users\Administrator\PycharmProjects\TensorFlowTest\venv\Scripts\chromedriver.exe')
option1 = webdriver.ChromeOptions
option2 = webdriver.ChromeOptions
# option1.add_argument("--user-data-dir=" + r"D:/ChromeDev/01")
# option2.add_argument("--user-data-dir=" + r"D:/ChromeDev/02")

driver = webdriver.Chrome(service=service )
# driver1 = webdriver.Chrome(service=service, chrome_options=option2)
url = 'https://shopee.tw/'
cookies_List = [
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164432.289078,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_E1H7XE0312",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GS1.1.1690603939.12.1.1690604432.0.0.0"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959584,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SPC_T_ID",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "evev25ma60T3c9eoR9gQ+3Sb5VMo0d8mf1K0IfDQXDDhL0RWtYbJ0gPXVbYPfnuhbSiPWQYkh4oyLy3S70qQwPrunEKchH3urlugPYzWmW9QckBHv5Nnn6TwZu/8LC+Ho9XaspEfjkytHCxSeg2Lrqs9pLKSkKxAfa7UpcZCmmQ="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724726600.570326,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SPC_F",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "iA3sueOkIOMuUj0DCaVJVD7wM0kLPhEJ"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959653,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SPC_R_T_ID",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "evev25ma60T3c9eoR9gQ+3Sb5VMo0d8mf1K0IfDQXDDhL0RWtYbJ0gPXVbYPfnuhbSiPWQYkh4oyLy3S70qQwPrunEKchH3urlugPYzWmW9QckBHv5Nnn6TwZu/8LC+Ho9XaspEfjkytHCxSeg2Lrqs9pLKSkKxAfa7UpcZCmmQ="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1690607803,
        "hostOnly": False,
        "httpOnly": False,
        "name": "AMP_TOKEN",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "%24NOT_FOUND"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1690690833.959602,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SPC_SI",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "sgO6ZAAAAABmUUFnM2NhUAQdHwAAAAAAOGg5c1RXdEQ="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1690604492,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_dc_gtm_UA-61915057-6",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "1"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959645,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SPC_EC",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "dXF6dFlqUjB2UFJWNFY0cSr3U4AgdwGIPYyODo+pdrRmAurkcqoZGxupUSGtJjTJKhN2UM9RjuSCySRYH8/LTGMeB/2ajfZI0Dlujxr6XSFEmjzhpcMYgarh4dasB/cOEdOls1S0QPY6XWFH/ShFN7PUjg5yN6G2s3ioVurcKnQ="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1698380432,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_fbp",
        "path": "/",
        "sameSite": "Lax",
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "fb.1.1676814906751.1198710341"
    },
    {
        "domain": "shopee.tw",
        "expirationDate": 1690635970,
        "hostOnly": True,
        "httpOnly": False,
        "name": "ds",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "eaec026a670ab74407da716a6f4af04b"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164432.289397,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GA1.1.1198329123.1652766030"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1717055156,
        "hostOnly": False,
        "httpOnly": False,
        "name": "__utma",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "88845529.1198329123.1652766030.1653983157.1653983157.1"
    },
    {
        "domain": "shopee.tw",
        "expirationDate": 1724652317.407902,
        "hostOnly": True,
        "httpOnly": False,
        "name": "fulfillment-language",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "zh-Hant"
    },
    {
        "domain": "shopee.tw",
        "hostOnly": True,
        "httpOnly": False,
        "name": "__LOCALE__'None'",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": True,
        "storeId": 'None',
        "value": "TW"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724726600.570761,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_02CL8MHLT0",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GS1.1.1681881236.5.1.1681881439.0.0.0"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724726600.570806,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_E4FV1WFT0L",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GS1.1.1678154944.2.0.1678154944.60.0.0"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724314806.650919,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_JD9WKB3ZNL",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GS1.1.1689754731.5.1.1689754806.60.0.0"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1721653223.254499,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_ga_RPSBE3TQZZ",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GS1.1.1687093219.61.0.1687093223.56.0.0"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1697942680,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gac_UA-61915057-6",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "1.1690166680.EAIaIQobChMIvfvuwqmmgAMVzdpMAh1CiwvtEAAYASAAEgLyefD_BwE"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1692931166,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_au",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "1.1.2146723379.1685155166"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1697942679,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gcl_aw",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GCL.1690166679.EAIaIQobChMIvfvuwqmmgAMVzdpMAh1CiwvtEAAYASAAEgLyefD_BwE"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1690690832,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_gid",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GA1.2.1281721519.1690604204"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1692758678,
        "hostOnly": False,
        "httpOnly": False,
        "name": "_med",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "cpc"
    },
    {
        "domain": "shopee.tw",
        "expirationDate": 1690635481,
        "hostOnly": True,
        "httpOnly": False,
        "name": "_QPWSDCXHZQA",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "f969d986-ea23-41dc-9401-3eb98eac2a1a"
    },
    {
        "domain": "shopee.tw",
        "hostOnly": True,
        "httpOnly": False,
        "name": "csrftoken",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": True,
        "storeId": 'None',
        "value": "xmDTNhCothHVKPcg4Q1xFFLFnNWOBYyD"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1702747537,
        "hostOnly": False,
        "httpOnly": False,
        "name": "cto_bundle",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "B969ul9jc085Y2FrdFBFaWN4YnhBUTJ4VzBQNTFVejI0dWE3NUNmM1hXaG1IRFhRQnJ6JTJGRWJhYTlZUVNiUHduOWFtRUNDOExTaFliVHh0MjJyRDRGQTdTZ2NkUnFqZEpIU0klMkJMVmpYWmNMWSUyRk5ORTh5Z1RadG9KRElxQm1jQkREdkxlVGE3ZHZBZHhyU1dVR2NLc0s4JTJCM0lHQSUzRCUzRA"
    },
    {
        "domain": "shopee.tw",
        "expirationDate": 1724726600.571342,
        "hostOnly": True,
        "httpOnly": False,
        "name": "fulfillment_language",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "zh-Hant"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724726600.571405,
        "hostOnly": False,
        "httpOnly": True,
        "name": "REC_T_ID",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "daff7c20-d5a3-11ec-9fd6-d09466041c35"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1724726600.571463,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SC_DFP",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "hM2kNZSea7VoOmlwuZbMRhwn6XcLwdZO"
    },
    {
        "domain": "shopee.tw",
        "expirationDate": 1690635970,
        "hostOnly": True,
        "httpOnly": False,
        "name": "shopee_webUnique_ccd",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "GUBV2EhclViNqEwtgkr49A%3D%3D%7CD8306WDUXeRqt0ylc8oS8Gehe2gS%2BCKyRH32zyINReVfD8syrrEGazrVGVAH2DOeWBC2eUidB2U%3D%7CusHoW76taamgGfu0%7C08%7C3"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1719715191.970405,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SPC_CLIENTID",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": False,
        "storeId": 'None',
        "value": "aUEzc3VlT2tJT011gptkwldyzthwvcvj"
    },
    {
        "domain": "shopee.tw",
        "hostOnly": True,
        "httpOnly": False,
        "name": "SPC_IA",
        "path": "/",
        "sameSite": 'None',
        "secure": False,
        "session": True,
        "storeId": 'None',
        "value": "1"
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959565,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SPC_R_T_IV",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "Y0NTUHBvV0VzdEJrczI0Tg=="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.95963,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SPC_ST",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": ".ektqN2FxZGY3Y0ZnRXpWVFZdsfGWk0T9W+rrC4Sv0Sh5xe67CXGkvZ+8KiksTSQoVrZRMoQ24/JuGjznUPgomL/qSc8rukrpqgkeoCgAHAc5cAFgmDvtvVtQlsXVc+nA2jrthhL0iUcqrlLTLgtglYTsih9cJ2l2wdiquoGymNMhYDy4klt0er7K5fruK+avMU7sTkd60XyUtAk3ckxxnw=="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959594,
        "hostOnly": False,
        "httpOnly": True,
        "name": "SPC_T_IV",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "Y0NTUHBvV0VzdEJrczI0Tg=="
    },
    {
        "domain": ".shopee.tw",
        "expirationDate": 1725164433.959638,
        "hostOnly": False,
        "httpOnly": False,
        "name": "SPC_U",
        "path": "/",
        "sameSite": 'None',
        "secure": True,
        "session": False,
        "storeId": 'None',
        "value": "35420973"
    }
]
title_img_list = [r'C:\Users\Administrator\Desktop\房租补贴\商品图片\1.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\2.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\3.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\4.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\5.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\6.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\7.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\8.jpg',
                  r'C:\Users\Administrator\Desktop\房租补贴\商品图片\9.jpg']

title_video = r'C:\Users\Administrator\Desktop\房租补贴\商品图片\1.mp4'

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


def download(file_path, picture_url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        'Content-Type': 'image/jpeg'
    }
    r = driver.get(picture_url)
    # r = requests.get(picture_url)
    with open(file_path, 'wb') as f:
        f.write(r.content)


def button_verify():
    button_sure = '確認'
    elem_type_sure = get_element(button_sure, 'button')
    if elem_type_sure.is_enabled():
        elem_type_sure.click()
        return True
    return False


def get_element(text, ele_type, ele_class=None, attempt=5):
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


def get_item(item_name):
    type_items = driver.find_elements(By.XPATH, "//div[@class='attribute-select-item']")
    for item in type_items:
        if item_name in item.text:
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


# 每日风控数据比对自动获取
def _main_():
    driver.get(url)
    for cookies in cookies_List:
        driver.add_cookie(cookie_dict=cookies)

    # 账号填充输入
    # driver.refresh()
    driver.get('https://seller.shopee.tw/portal/product/new')
    verify_load(100)
    for img in title_img_list:
        elem_upload_input = driver.find_element(By.XPATH, '//input[@accept="image/*"]')
        elem_upload_input.send_keys(img)
        time.sleep(3)
    elem_upload_input = driver.find_element(By.XPATH, '//input[@accept="video/mp4"]')
    elem_upload_input.send_keys(title_video)
    time.sleep(3)
    button_verify()
    element_input = driver.find_element(By.XPATH, '//input[@placeholder="請輸入"]')
    goods_name = '耐打球头尼龙羽毛球塑料室外训练球耐用弹力防风塑料羽毛球拍配件'

    cc = opencc.OpenCC('s2t')
    goods_name = cc.convert(goods_name)
    element_input.send_keys(goods_name)
    elem_goods_type = driver.find_element(By.XPATH, "//span[contains(text(), '請選擇商品分類')]/..")
    elem_goods_type.click()
    time.sleep(1)
    type_first = '戶外與運動用品'
    elem_type_first = get_element(type_first, 'p')
    elem_type_first.click()
    time.sleep(1)
    type_two = '運動服飾/戶外服飾'

    elem_type_two = get_element(type_two, 'p')
    elem_type_two = select_other(elem_type_two)
    elem_type_two.click()
    time.sleep(1)
    if button_verify() is False:
        type_three = '泳裝/潛水服飾'
        elem_type_three = get_element(type_three, 'p')
        elem_type_three = select_other(elem_type_three)
        elem_type_three.click()
        time.sleep(2)
        if button_verify() is False:
            type_four = '比基尼'
            elem_type_four = get_element(type_four, 'p')
            elem_type_four = select_other(elem_type_four)
            elem_type_four.click()
            time.sleep(1)
            button_verify()
    time.sleep(2)
    input_Description = '請輸入商品描述或點選以新增圖片'
    elem_type_sure = driver.find_element(By.XPATH, "//div[@data-placeholder='{}']".format(input_Description))

    elem_type_sure.send_keys(description_str)
    elem_description_img = driver.find_element(By.XPATH, "//input[@accept='image/jpg,image/jpeg,image/png']")

    for i in range(3):
        elem_description_img.send_keys(title_img_list[i])
        time.sleep(3)
    # driver.find_elements(By.XPATH, "//div[@class='attribute-select-item']")[1].find_element(By.XPATH,
    #                                                                                         "//span[contains(text(), '尼龍')]/..").find_element( By.TAG_NAME, 'svg').click()

    for attribute in class_attribute_List:
        if attribute['vn'] != '':
            item_ele = get_item(attribute['n'])
            item_ele.click()
            time.sleep(3)
            item_ele.find_element(By.XPATH, "//div[contains(text(), '{}')]".format(attribute['vn'])).click()
            time.sleep(3)
        # item_ele.send_keys(attribute['vn'])
    driver.find_element(By.XPATH, "//span[contains(text(),'開啟商品規格')]/..").click()
    time.sleep(3)
    for row in googds_infos[0]['dataRows']:
        row['name']
        row['specValue']['name']
        row['specValue']['simage']
    download('d:/private/1.jpg', 'https://s-cf-sg.shopeesz.com/file/d807f7e8e2804251fab15d11768ca889')
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[contains(text(),'【黑色】+軟質升降扶手+靠背可躺')]").find_element(By.XPATH,
                                                                                                         "//input[@accept='image/*']").send_keys(
        'https://s-cf-sg.shopeesz.com/file/d807f7e8e2804251fab15d11768ca889')
    driver.quit()
    service.stop()
    time.sleep(0.1)
    # os.system(r'start "" /d "C:\Program Files (x86)\Notepad++" /wait "notepad++.exe" "./log/20220824.txt"')
    # win32api.ShellExecute(0, 'open', r'C:\Program Files (x86)\Notepad++\notepad++.exe', path, '', 1)
    sys.exit()


def base64_to_image(base64_str):
    base64_data = re.sub('^data:image/.+;base64,', '', base64_str)
    byte_data = base64.b64decode(base64_data)
    image_data = BytesIO(byte_data)
    img = Image.open(image_data)
    return img


def download_img():
    js = "let c = document.createElement('canvas');let ctx = c.getContext('2d');" \
         "let img = document.getElementsByTagName('img')[0]; /*找到图片*/ " \
         "c.height=img.naturalHeight;c.width=img.naturalWidth;" \
         "ctx.drawImage(img, 0, 0,img.naturalWidth, img.naturalHeight);" \
         "let base64String = c.toDataURL();return base64String;"

    base64_str = driver.execute_script(js)
    img = base64_to_image(base64_str)
    rgb_im = img.convert('RGB')
    rgb_im.save('d:/private/1.jpg')


if __name__ == '__main__':
    try:
        # download('d:/private/1.jpg', 'https://s-cf-sg.shopeesz.com/file/d807f7e8e2804251fab15d11768ca889')
        # os.remove('d:/private/img1.jpg')
        # urllib_download()
        # driver.get('https://s-cf-sg.shopeesz.com/file/d807f7e8e2804251fab15d11768ca889')
        # download_img()
        _main_()


    except Exception as ex:
        traceback.print_exc()
        driver.quit()
        service.stop()
        sys.exit()
