import datetime
import json
import os
import random
import sys
import time
import traceback
import requests

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
    'Origin': 'https://item.jd.com'
    # 'Cookie': 'shshshfpa=a4036330-9ac6-f2d7-5bdc-812543da7734-1690178502; shshshfpx=a4036330-9ac6-f2d7-5bdc-812543da7734-1690178502; __jdc=122270672; __jdv=122270672|direct|-|none|-|1690178503053; 3AB9D23F7A4B3C9B=RF7TH6Q3EPUBKKCQ2OYI5OH3RK4ZRTJ7GZQ6PC4CB4R7M22LMGX2YVBLOC3DY2SXDT6AKS7OKQUXNQF5X7OQL6RV5I; shshshfpb=rE2uxVGfOIrhEhaSN7I6CtA; areaId=2; __jdu=1690178503053154636277; ipLoc-djd=2-2813-61125-0; jsavif=1; 3AB9D23F7A4B3CSS=jdd03RF7TH6Q3EPUBKKCQ2OYI5OH3RK4ZRTJ7GZQ6PC4CB4R7M22LMGX2YVBLOC3DY2SXDT6AKS7OKQUXNQF5X7OQL6RV5IAAAAMJQ3DKEYAAAAAADBCO3QKAUTVN7UX; _gia_d=1; __jda=122270672.1690178503053154636277.1690178503.1690178503.1690183312.2; token=e16be163663272bbd7dfdc839975f54a,2,938990; __tk=0389e34022cf7e78f7e3b5167f896a34,2,938990; __jdb=122270672.2.1690178503053154636277|2.1690183312'
}
enable = True
sckey = 'SCT217112TYc3y947VdAioG3AjfVDuY1Zb'
proxies = []


def get_total_milliseconds(exec_date):
    current = exec_date - datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m-%d %H:%M')
    return int(current.total_seconds() * 1000)


def get_datetime(milliseconds):
    current = datetime.timedelta(milliseconds=milliseconds) + datetime.datetime.strptime('1970-01-01 08:00', '%Y-%m'
                                                                                                             '-%d '
                                                                                                             '%H:%M')
    return current


def get_random_ip():
    if len(proxies) == 0:
        return None
    proxy_ip = random.choice(proxies)
    proxy = json.loads(proxy_ip)
    return proxy


urls = [{'url': url, 'goods_no': 100011488878}
    , {'url': two_url, 'goods_no': 100046206079}
    , {'url': three_url, 'goods_no': 100057529076}
        # ,{'url': four_url, 'goods_no': 100038651615}
    # , {'url': five_url, 'goods_no': 100026081829}
        ]


def _main_():
    file_path = 'proxies' + '.txt'
    if os.path.exists(file_path):
        with open(file_path, "r", encoding='utf8') as f:
            proxies = f.readlines()
            for i in range(len(proxies)):
                proxies[i] = proxies[i].replace('\n', '')

            f.close()

    while True:
        randint_time = random.randint(5 * 1000, 20 * 1000)

        start = time.perf_counter()
        requests.packages.urllib3.disable_warnings()
        for url in urls:
            url['status'] = 0
            total_seconds = get_total_milliseconds(datetime.datetime.now())
            headers['x-referer-page'] = 'https://item.jd.com/{}.html'.format(url['goods_no'])
            for i in range(10):
                response = requests.get(url['url'].format(total_seconds), headers=headers, proxies=get_random_ip(),
                                        verify=False)
                if response.status_code == 403:
                    # print('403报错')
                    continue
                else:
                    break
            if response.status_code == 403:
                continue
            result = response.content.decode('utf-8')
            try:
                result_json = json.loads(result)
                status_str = result_json['stockInfo']['stockDesc']
                name_str = result_json['wareInfo']['wname']
                goods_id = result_json['wareInfo']['wareId']
            except:
                print(result)
                traceback.print_exc()
                continue
            # index = result.find('<strong>')
            # status_str = result[index + 8:index + 10]
            url['status'] = 1 if '无货' not in status_str else 0
            status_str = '有货' if '无货' not in status_str else '无货'
            name_str = str(name_str).split(' ')[0]
            # print('当前时间：{}，商品：{}，{}'.format(datetime.datetime.now(), url['goods_no'], status_str))
            print('当前时间：{}，商品：{}，状态：{}，名称：{}'.format(datetime.datetime.now(), goods_id, status_str, name_str))
            if status_str == '有货':
                notify_str = '商品{}有货啦'.format(goods_id)
                resp = requests.get(
                    'https://sc.ftqq.com/{}.send?text={}&desp={}'.format(sckey, notify_str, notify_str)
                )
                resp_json = json.loads(resp.text)
        end = time.perf_counter()
        print('耗时：{:.4f}s'.format(end - start))
        print('等待：{:.4f}s'.format(randint_time / 1000))
        time.sleep(randint_time / 1000)


if __name__ == '__main__':
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
