import sys
import datetime
import traceback

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Cookie': 'acw_tc=7250b3a016788687671997856e87fe698cc15da1d840e8d04fc10b863d; qcc_did=666271c2-1fa8-45b0-8b29-ad0867e660cd; QCCSESSID=cf57deefa1465bcbb00d94cca7'
}

url = 'https://www.qcc.com/web/search?key={}'
frim_url = 'https://www.qcc.com/firm/{}.html'
keys = []
result_list = []


def write_txt(log):
    curr_date_str = datetime.datetime.today().strftime('%Y-%m-%d')
    with open(curr_date_str + '_company.txt', 'w', encoding='utf8') as w:
        for item in log:
            w.write(str(item) + '\n')
        w.close()


def _main_():
    requests.packages.urllib3.disable_warnings()
    with open("key.txt", "r", encoding='utf8') as f:
        keys = f.readlines()
        f.close()
    for item in keys:
        key = item.replace('\n', '')
        result_response = requests.get(url.format(key), verify=False, headers=headers)
        result_response.encoding = 'utf-8'
        keyNo_index = result_response.text.find('KeyNo')
        name_index = result_response.text.find('Name', keyNo_index)
        Type_index = result_response.text.find('Type', name_index)
        frim_no = result_response.text[keyNo_index:name_index].replace('"', '').replace(',', '').replace('KeyNo:', '')
        name_str = result_response.text[name_index:Type_index].replace('"', '').replace(',', '').replace('Name:', '')
        result_response = requests.get(frim_url.format(frim_no), verify=False, headers=headers)
        result_response.encoding = 'utf-8'
        temp = 'alt="qcc" class="gm-img"><span class="val">'
        first_index = result_response.text.find(temp)
        size = result_response.text[first_index + len(temp):first_index + len(temp) + 2]
        result_list.append({'name': name_str, 'key': key, 'size': size})
        print('公司名称:{},统一社会信用代码:{},规模:{}'.format(name_str, key, size))
    write_txt(result_list)


if __name__ == '__main__':
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
