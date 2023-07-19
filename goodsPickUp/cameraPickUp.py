import random
import sys
import time

import requests
import datetime
import urllib.request

from config import proxies, verify_str

# 100011488878
url = 'https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={}&body=%7B%22skuId%22%3A100011488878%2C%22cat%22%3A%22652%2C654%2C831%22%2C%22area%22%3A%222_2813_61126_0%22%2C%22shopId%22%3A%221000000858%22%2C%22venderId%22%3A1000000858%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%22100000000001%5C%22%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppp2p1ppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&h5st=20230718165111486%3B8656582560057196%3Bfb5df%3Btk03wb1d21c2918ndq18yiG8eo0LZZcvic4pUy6fW2jg8nRG4he1cw4_gkj4KfZUzb5feDWMFB0dlHNKpa5rU3wAYQZQ%3Bf181857ac1456d1a35f079404aefaab81249ac0abb153303bcd2cf3ba832d958%3B3.1%3B1689670271486%3B24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e34bc39582ed3ca02a8625831e475b0500fa9547df63a2887c8e7f06415e95f9ac90be8ac46f1409dc5c72568820e2979bb89f1eed5e203d21f18d6ca9773e84c3&x-api-eid-token=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNAZEDBAAAAAAD2KKH624RE3XY4X&loginType=3&uuid=122270672.1679626950385406120060.1679626950.1689666377.1689670082.13'
# https://item.jd.com/100046206079.html
two_url = 'https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={}&body=%7B%22skuId%22%3A100046206079%2C%22cat%22%3A%22652%2C654%2C5012%22%2C%22area%22%3A%222_2813_61126_0%22%2C%22shopId%22%3A%221000000858%22%2C%22venderId%22%3A1000000858%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%221%5C%22%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppp2pppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&h5st=20230718170418479%3B8656582560057196%3Bfb5df%3Btk03wb1d21c2918ndq18yiG8eo0LZZcvic4pUy6fW2jg8nRG4he1cw4_gkj4KfZUzb5feDWMFB0dlHNKpa5rU3wAYQZQ%3B5b56b2b3e2d60f459e91300f038c9fff8302de1c706ed28bd275f939ab32a647%3B3.1%3B1689671058479%3B24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e34bc39582ed3ca02a8625831e475b0500fa9547df63a2887c8e7f06415e95f9ac90be8ac46f1409dc5c72568820e2979bb89f1eed5e203d21f18d6ca9773e84c3&x-api-eid-token=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNA62M7QAAAAADW2BKER35C2VCMX&loginType=3&uuid=122270672.1679626950385406120060.1679626950.1689666377.1689670082.13'
# https://item.jd.com/100057529076.html
three_url = 'https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={}&body=%7B%22skuId%22%3A100057529076%2C%22cat%22%3A%22652%2C654%2C5012%22%2C%22area%22%3A%222_2813_61126_0%22%2C%22shopId%22%3A%221000000858%22%2C%22venderId%22%3A1000000858%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%221%5C%22%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppppppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&h5st=20230718170531039%3B8656582560057196%3Bfb5df%3Btk03wb1d21c2918ndq18yiG8eo0LZZcvic4pUy6fW2jg8nRG4he1cw4_gkj4KfZUzb5feDWMFB0dlHNKpa5rU3wAYQZQ%3Bf341f60b62b13d981566aa447cbe232e33cfc639cd1dcf99e588868fce08ca6b%3B3.1%3B1689671131039%3B24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e34bc39582ed3ca02a8625831e475b0500fa9547df63a2887c8e7f06415e95f9ac90be8ac46f1409dc5c72568820e2979bb89f1eed5e203d21f18d6ca9773e84c3&x-api-eid-token=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNA62M7QAAAAADW2BKER35C2VCMX&loginType=3&uuid=122270672.1679626950385406120060.1679626950.1689666377.1689670082.13'
# https://item.jd.com/100038651615.html
four_url = 'https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={}&body=%7B%22skuId%22%3A100038651615%2C%22cat%22%3A%22652%2C654%2C5012%22%2C%22area%22%3A%222_2813_61126_0%22%2C%22shopId%22%3A%221000000858%22%2C%22venderId%22%3A1000000858%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%22100000000001%5C%22%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppp2pppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&h5st=20230718170610688%3B8656582560057196%3Bfb5df%3Btk03wb1d21c2918ndq18yiG8eo0LZZcvic4pUy6fW2jg8nRG4he1cw4_gkj4KfZUzb5feDWMFB0dlHNKpa5rU3wAYQZQ%3B0442eae9cdc5b19d10edb0fc6c76a13b71ced745d85ba5ceaf8e487234ecaeb0%3B3.1%3B1689671170688%3B24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e34bc39582ed3ca02a8625831e475b0500fa9547df63a2887c8e7f06415e95f9ac90be8ac46f1409dc5c72568820e2979bb89f1eed5e203d21f18d6ca9773e84c3&x-api-eid-token=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNA77WSIAAAAACIU5MNZQEVBJBEX&loginType=3&uuid=122270672.1679626950385406120060.1679626950.1689666377.1689670082.13'
# https://item.jd.com/100026081829.html
five_url = 'https://api.m.jd.com/?appid=pc-item-soa&functionId=pc_detailpage_wareBusiness&client=pc&clientVersion=1.0.0&t={}&body=%7B%22skuId%22%3A100026081829%2C%22cat%22%3A%22652%2C654%2C5012%22%2C%22area%22%3A%222_2813_61126_0%22%2C%22shopId%22%3A%221000000858%22%2C%22venderId%22%3A1000000858%2C%22paramJson%22%3A%22%7B%5C%22platform2%5C%22%3A%5C%221%5C%22%2C%5C%22specialAttrStr%5C%22%3A%5C%22p0ppppppppp2pppppppppppppp%5C%22%2C%5C%22skuMarkStr%5C%22%3A%5C%2200%5C%22%7D%22%2C%22num%22%3A1%2C%22bbTraffic%22%3A%22%22%7D&h5st=20230718171407344%3B8656582560057196%3Bfb5df%3Btk03wb1d21c2918ndq18yiG8eo0LZZcvic4pUy6fW2jg8nRG4he1cw4_gkj4KfZUzb5feDWMFB0dlHNKpa5rU3wAYQZQ%3Bd8eba36ee189ecd0eb9d314d17fd0d16141d6aac01a70f83f85ee4de795a3ed2%3B3.1%3B1689671647344%3B24c9ee85e67cf80746dd82817ecbeafc7a829b35c7f446a4c7d476cc9faa1d8834a93323ad7bce9bef1bba682b93d2e34bc39582ed3ca02a8625831e475b0500fa9547df63a2887c8e7f06415e95f9ac90be8ac46f1409dc5c72568820e2979bb89f1eed5e203d21f18d6ca9773e84c3&x-api-eid-token=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNBDT7IYAAAAADLLCD4U3ZA5KIYX&loginType=3&uuid=122270672.1679626950385406120060.1679626950.1689666377.1689670082.13'
headers = {
    'Host': 'api.m.jd.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://item.jd.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'x-referer-page': 'https://item.jd.com/100011488878.html',
    'x-rp-client': 'h5_1.0.0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'sec-ch-ua-platform': '"Windows"',
    'Origin': 'https://item.jd.com',
    'Cookie': 'shshshfp=3ca8d90768d753a9460997379fede5c5; shshshfpa=0b14f600-7fa9-5f77-ea1b-d01b785afbf2-1679626952; shshshfpx=0b14f600-7fa9-5f77-ea1b-d01b785afbf2-1679626952; __jdu=1679626950385406120060; b_dw=1903; b_dh=929; b_dpr=1; b_webp=1; b_avif=1; __jdv=122270672|direct|-|none|-|1689642629326; pinId=3IJspHBOu-K1ffsfn98I-w; pin=dq2651yf; unick=%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%8A%E5%95%AA; _tp=%2BHpn2tzm%2B5tpuqDNmwSjnw%3D%3D; _pst=dq2651yf; shshshfpb=hCZx4GwUO6fE5Ipv5RwDCdg; PCSYCityID=CN_310000_310100_0; __jdc=122270672; areaId=2; ipLoc-djd=2-2813-61126-0; jsavif=1; wxa_level=1; retina=0; cid=9; jxsid=16896606130166028279; webp=1; mba_muid=1679626950385406120060; visitkey=30024700555322058; equipmentId=Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3A; deviceVersion=114.0.0.0; deviceOS=; deviceOSVersion=; deviceName=Chrome; sc_width=1920; warehistory="100011488878,100011488878,100011488878,"; fingerprint=0brlZBzjwkyTCUUAqaDggG6YeMrOP4Kc; autoOpenApp_downCloseDate_autoOpenApp_autoPromptly=1689660634291_1; __jd_ref_cls=MDownLoadFloat_AppArouseA1; __wga=1689660634333.1689660616424.1689660616424.1689660616424.3.1; PPRD_P=UUID.1679626950385406120060-LOGID.1689660634338.1629633496; __jda=122270672.1679626950385406120060.1679626950.1689663649.1689666377.12; wlfstk_smdl=2abjea057yon50chwzd3t12r55uly3l0; TrackID=1B85UmDYhVti4z-vNpfzIfI9iGYpHf5rf-W8m-gKoYRqJy-19XWbnnQy6DXX1iq5LyDiv7wjlP8YeSB-INYlrNPDIkl7tKNVBfJa9jHhVfSY; thor=0922FE7FC0B23FFBA61FE794A8CD909E8059A09F1C9E68DAF9EF267E3339D6C7AAE583843CA65A0BFBC8AD52766425E828E0C1AB27F38C8414BE8CBD7FC75505D4E0DC881144E269D0B45D5903DDC4A957E5689C07E69B74600E4F95C04185851A0EDDC5F0AE38843763177C14DB62CED850BF0B8119ABA2C0C5160E0CBDE650DFE57868DE414B400F1015274BB0DB15; flash=2_mJGbvNN8qm0irPQGOFgzJGW4fAgf6GsYLq1d-FNIvDdWvkJpO_3eC1O89VM7Z2lmqjwyiOqSBM2mvbXd3XCSNiqUtyMKDoVJkT__Ms0trZL*; ceshi3.com=201; token=c4641aa113487395477805716fb79b47,3,938704; __tk=iUyEV0AEixzynleDixnEVMaCnZoFnMzwiZoEnDj5ilVwixaNR0nNnX,3,938704; 3AB9D23F7A4B3CSS=jdd03Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3AAAAAMJNAFNHOYAAAAADTNHWJA4T6GOBEX; _gia_d=1; 3AB9D23F7A4B3C9B=Q3VNOGVW67BGBYBSMCR2FNHHJKH5SYZ4GSQROUGQPGOEUQAAPYOGJM3SNYB56NXEN24OW3ZI2ZC2FI2SAQQ56LOD3A; __jdb=122270672.9.1679626950385406120060|12.1689666377'
}


def get_total_milliseconds(exec_date):
    current = exec_date - datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m-%d %H:%M')
    return int(current.total_seconds() * 1000)


def get_datetime(milliseconds):
    current = datetime.timedelta(milliseconds=milliseconds) + datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m'
                                                                                                             '-%d '
                                                                                                             '%H:%M')
    return current


urls = [{'url': url, 'goods_no': 100011488878}, {'url': two_url, 'goods_no': 100046206079},
        {'url': three_url, 'goods_no': 100057529076}, {'url': four_url, 'goods_no': 100038651615},
        {'url': five_url, 'goods_no': 100026081829}]
for j in range(20):
    randint_time = random.randint(10 * 1000, 60 * 1000)

    start = time.perf_counter()
    for url in urls:
        url['status'] = 0
        total_seconds = get_total_milliseconds(datetime.datetime.now())
        for i in range(10):
            response = requests.get(url['url'].format(total_seconds), headers=headers, proxies=proxies,
                                    verify=verify_str)
            if response.status_code == 403:
                # print('403报错')
                continue
            else:
                break
        result = response.content.decode('utf-8')
        index = result.find('<strong>')
        status_str = result[index + 8:index + 10]
        url['status'] = 1 if status_str != '无货' else 0
        print('当前时间：{}，商品：{}，{}'.format(datetime.datetime.now(), url['goods_no'], status_str))
    end = time.perf_counter()
    print('耗时：{:.4f}s'.format(end - start))
    print('等待：{:.4f}s'.format(randint_time / 1000))
    time.sleep(randint_time / 1000)

#
# start = time.perf_counter()
#
# req=urllib.request.Request(url.format(total_seconds),headers=headers)
# resp=urllib.request.urlopen(req)
# data=resp.read().decode('utf-8')
# index=data.find('<strong>')
# # print(data)
# print(data[index+8:index+10])
# end = time.perf_counter()
# print('耗时：{:.4f}s'.format(end - start))
sys.exit()
