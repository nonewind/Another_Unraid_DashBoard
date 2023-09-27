# -*- encoding: utf-8 -*-
'''
@File    :   unraid.py
@Time    :   2023/09/25 14:13:28
@Author  :   Zhangziheng 
'''

import re

import requests
import websocket
from ..utils.logger import creatLogger

requests.packages.urllib3.disable_warnings()


class UnraidApi(object):
    def __init__(self, username, password, baseUrl) -> None:
        self.username = username
        self.password = password
        self.cookies = ''
        self.baseUrl = baseUrl
        self.logger = creatLogger("UnraidApi")
        self.crsfToekn = ""

    def upsLoad(self, type) -> websocket.WebSocketApp:
        """获取ups的负载情况
        
        Returns:
            websocket.WebSocketApp: _description_
        """
        return self._extracted_getWSData(type, '/sub/apcups')

    def cpuLoad(self, type) -> websocket.WebSocketApp:
        """获取cpu负载、网速

        Returns:
            websocket.WebSocketApp: _description_
        """
        return self._extracted_getWSData(
            type, '/sub/cpuload,update1,update2,update3')

    # TODO Rename this here and in `upsLoad` and `cpuLoad`
    def _extracted_getWSData(self, type, arg1) -> websocket.WebSocketApp:
        """提取的方法

        Args:
            type (_type_): _description_
            arg1 (_type_): _description_

        Returns:
            websocket.WebSocketApp: _description_
        """
        if type == 1:
            url = f'wss://{self.baseUrl}{arg1}'
        else:
            url = f'ws://{self.baseUrl}{arg1}'
        header = {'cookie': self.cookies}
        ws = websocket.create_connection(url=url, header=header)
        return ws

    def _login(self, type) -> bool:
        """
        login with username and pwd to get hedaer token
        """
        data = {'username': self.username, 'password': self.password}
        if type == 1:
            login_url = f'https://{self.baseUrl}/login'
        else:
            login_url = f'http://{self.baseUrl}/login'
        try:
            session = requests.post(url=login_url,
                                    data=data,
                                    timeout=(10, 10),
                                    allow_redirects=False)
        except Exception as e:
            self.logger.error(f"Login Error: {e}")
            return False
        # 如果不是302 就代表密码错误
        if session.status_code != 302:
            self.logger.error("Login Error:  Maybe Ur Password Error")
            return False
        # Get cookies
        unraidHeaderToken = session.cookies.get_dict()
        for k, v in unraidHeaderToken.items():
            _cookie = f"{k}={v};"
            self.cookies += _cookie
        # Get crsfToken
        if type == 1:
            Dashboard_url = f'https://{self.baseUrl}/Dashboard'
        else:
            Dashboard_url = f'http://{self.baseUrl}/Dashboard'
        header = {'cookie': self.cookies}
        try:
            req_session = requests.get(url=Dashboard_url,
                                       headers=header,
                                       timeout=(10, 10)).text
        except Exception as e:
            self.logger.error(f"Get crsfToekn Error: {e}")
            return False
        re_bat = r"var csrf_token = \"[\S]+?\";"
        re_bat_serverName = r"section[\"|']>([\S\s]+?)<br>"
        self.serverName = re.findall(re_bat_serverName, req_session)[0]
        try:
            self.crsfToekn = re.findall(re_bat, req_session)[0].split('"')[1]
            return True
        except Exception as e:
            return False