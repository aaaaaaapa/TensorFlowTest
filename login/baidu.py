#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import time
from uuid import uuid4
from getpass import getpass

import requests

from util import *


class BaiduLogin(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/601.2.7 (KHTML, like Gecko) Version/9.0.1 Safari/601.2.7',
            'referer': 'https://jywg.18.cn/Login?el=1&clear=1',
        }
        self.sess = requests.session()
        self.gid = str(uuid4()).upper()
        self.token = None
        self.key = None
        self.public_key = None

    def _init_cookies(self):
        """初始化cookies
        :return:
        """
        self.sess.get(url='https://pan.baidu.com/', headers=self.headers)

    def _get_token(self):
        """获取登陆token
        :return:
        """
        url = 'https://passport.baidu.com/v2/api/?getapi'
        payload = {
            'getapi': '',
            'tpl': 'mn',
            'apiver': 'v3',
            'tt': str(int(time.time() * 1000)),
            'class': 'login',
            'gid': self.gid,
            'loginversion': 'v4',
            'logintype': 'dialogLogin',
            'traceid': '',
            'callback': 'bd__cbs__pivyke',
        }
        resp = self.sess.get(url=url, params=payload, headers=self.headers)
        js = parse_json(resp.text.replace("\'", "\""))
        self.token = js['data']['token']

    def _get_public_key(self):
        """获取RSA公钥
        :return: RSA公钥
        """
        self.key, self.public_key = "-----BEGIN PUBLIC KEY-----\n" + "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDHdsyxT66pDG4p73yope7jxA92\n" + "c0AT4qIJ/xtbBcHkFPK77upnsfDTJiVEuQDH+MiMeb+XhCLNKZGp0yaUU6GlxZdp\n" + "+nLW8b7Kmijr3iepaDhcbVTsYBWchaWUXauj9Lrhz58/6AE/NF0aMolxIGpsi+ST\n" + "2hSHPu3GSXMdhPCkWQIDAQAB\n" + "-----END PUBLIC KEY-----";


    def login(self, username, password, retry=4):
        """用户名密码登陆
        :param username: 用户名
        :param password: 密码
        :return:
        """

        self._init_cookies()
        self._get_token()
        self._get_public_key()

        url = 'https://jywg.18.cn/Login/Authentication?validatekey='
        data = {
            'userId': username,
            'password': encrypt_pwd(password, self.public_key),
            'randNumber': 0.09490489122308454,
            'identifyCode': 8688,
            'duration': 30,
            'authCode': '',
            'type': 'Z'

        }

        for _ in range(retry):
            resp = self.sess.post(url=url, headers=self.headers, data=data)

            m = re.search('.*href \+= "(.*)"\+accounts', resp.text)
            result = m.group(1)
            d = dict([x.split("=") for x in result.split("&")])

            err_no = d.get('err_no')
            if err_no == '0':
                print('Login success！')
                return
            elif err_no in ['6', '257']:
                code_string = d.get('codeString')
                data['codestring'] = code_string
                resp = self.sess.get(
                    url='https://passport.baidu.com/cgi-bin/genimage?{}'.format(code_string),
                    headers=self.headers
                )
                image_path = os.path.join(os.getcwd(), 'vcode-login.jpg')
                save_image(resp, image_path)
                open_image(image_path)
                verify_code = input('Please enter the verify code for login(return change):')
                data['verifycode'] = verify_code
            elif err_no == '120021':
                raise LoginError("Account is in risk, please do security verification first!")
            elif err_no in ['4', '7']:
                raise LoginError('Error username or password!')
            else:
                raise LoginError("Unknown error:" + result)

        raise LoginError('Login Fail！')


class LoginError(Exception):
    pass


if __name__ == '__main__':
    username = input("Username: ")
    password = getpass("Password: ")
    b = BaiduLogin()
    b.login(username=username, password=password)
