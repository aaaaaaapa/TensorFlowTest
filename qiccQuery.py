import sys
import datetime
import traceback

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
    'Cookie': 'qcc_did=666271c2-1fa8-45b0-8b29-ad0867e660cd; QCCSESSID=f1a0c74324b981fa18ae29b2bd; acw_tc=77a7a82216856926528918261ed358e3b03723fbbaa439d57de4caa25b'
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
        frim_no_index = result_response.text.find('https://www.qcc.com/firm/')
        temp_text=result_response.text[frim_no_index:frim_no_index+100].replace('https://www.qcc.com/firm/', '')
        html_index=temp_text.find('.html')
        frim_no=temp_text[0:html_index]
        # name_index = result_response.text.find('Name', keyNo_index)
        # Type_index = result_response.text.find('Type', name_index)
        # frim_no = result_response.text[keyNo_index:name_index].replace('"', '').replace(',', '').replace('KeyNo:', '')
        # name_str = result_response.text[name_index:Type_index].replace('"', '').replace(',', '').replace('Name:', '')
        result_response = requests.get(frim_url.format(frim_no), verify=False, headers=headers)
        result_response.encoding = 'utf-8'
        company_name=result_response.text.split('企业名称')[1].split('<span class="copy-value">')[1].split('</span>')[0]
        company_size=result_response.text.split('企业规模')[1].split('<span class="val">')[1].split('</span>')[0]
        national_standard=result_response.text.split('国标行业')[1].split('<span>')[1].split('</span>')[0]

        result_list.append({'name': company_name, 'key': key, 'size': company_size,'national_standard':national_standard})
        print('公司名称:{},统一社会信用代码:{},企业规模:{},国标行业：{}'.format(company_name, key, company_size,national_standard))
    write_txt(result_list)


if __name__ == '__main__':
    try:
        _main_()
    except:
        traceback.print_exc()
    print('按回车键退出')
    input()
    sys.exit()
