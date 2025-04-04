# !/usr/bin/env python3
# router_client.py
import datetime
import re
import sys
import time

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import MaxRetryError

from router.config import REQUEST_TIMEOUT, load_config
from router.exceptions import (
    InvalidCredentialsError,
    MemoryIsOverflow_Exception,
    token_err,
)
from router.notification import LINENotifyBot


class router_client:
    def __init__(
        self,
        ID: str,
        PASSWD: str,
        IP: str,
        LINE_ACCESS_TOKEN: str,
        CHANNEL_ID: str,
        MY_PHONE_NUM: int = 0,
        IGNORE_PHONENUM: int = 0,
    ):
        self.__BASE_URL = load_config(IP)["__BASE_URL"]
        self.__MAIN_PATH = load_config(IP)["__MAIN_PATH"]
        self.__SUB_PATH_BASIC_V4PPPOE = load_config(IP)["__SUB_PATH_BASIC_V4PPPOE"]
        self.__CALL_HIS = load_config(IP)["__CALL_HIS"]
        self.__LINE_ACCESS_TOKEN = LINE_ACCESS_TOKEN
        self.__CHANNEL_ID = CHANNEL_ID
        self.__MY_PHONE_NUM = MY_PHONE_NUM
        self.__IGNORE_PHONE_NUM = IGNORE_PHONENUM
        self.session = requests.Session()
        headers = {"referer": self.__BASE_URL, "user-agent": None}
        auth = (ID, PASSWD)
        self.post_kwargs = dict(
            headers=headers, timeout=REQUEST_TIMEOUT, data=None, cookies=None, auth=auth
        )

    def callHistory(self) -> None:
        CALL_HIS_PATH = r"..//CALL_HIS_PATH.txt"
        with open(CALL_HIS_PATH, mode="r", encoding="utf8") as CALL_HIS_LIS:
            callHisLisOpen = CALL_HIS_LIS.read()
        try:
            called = self.session.get(
                self.__BASE_URL + self.__MAIN_PATH + self.__CALL_HIS, **self.post_kwargs
            )
        except Exception as e:
            if "WinError 10055" in str(e):
                raise MemoryIsOverflow_Exception()
            print("ConnectionError_" + str(e.args))
            time.sleep(2)
            return self.ipChange()
        if called.status_code != 200:
            raise InvalidCredentialsError()
        html = called.text
        try:
            CallLis = html.split("There are 100 entries.\n\n", 1)[1].split("</pre>", 1)[
                0
            ]
            CallLis = re.sub(r"^.....", "", CallLis)
            CallList: list[str] = re.sub(r"\n.....", "\n", CallLis).splitlines()
            for CallLi in CallList:
                if CallLi in callHisLisOpen:
                    pass
                else:
                    with open(CALL_HIS_PATH, mode="a", encoding="utf8") as f:
                        f.write(CallLi + "\n")
                        if "発信" in CallLi:
                            call_arriveORsend = "【発信】しました。\n"
                            print("発信有り")
                        elif "着信" in CallLi:
                            call_arriveORsend = "【着信】がありました。\n"
                            print("着信有り")
                        else:
                            call_arriveORsend = "宛先不明が不明です。\n"
                        CallLi = re.sub(r" 1 TEL1 - - - -", "", CallLi)
                        CallLi = re.sub(r" - - - - - -", "", CallLi)
                        CallLi = re.sub(r" - - - - 1 TEL1 0 -", "", CallLi)
                        CallLi = re.sub(r" - ", "\n", CallLi)
                        CallLi = re.sub(r" 接続先切断", "\n接続先切断", CallLi)
                        CallLi = re.sub(r" 自切断", "\n自切断", CallLi)
                        CallLi = re.sub(r" 宛先不明", "\n宛先不明", CallLi)
                        CallLi = re.sub(
                            r" " + str(self.__MY_PHONE_NUM) + " ",
                            "\nhttps://www.google.com/search?q=",
                            CallLi,
                        )
                        print(
                            "\n更新時間"
                            + str(datetime.datetime.now())
                            + "\n"
                            + call_arriveORsend
                            + CallLi
                            + "\n"
                        )
                        if (
                            "ユーザ拒否(P)" in CallLi
                            or str(self.__IGNORE_PHONE_NUM) in CallLi
                        ):
                            print(
                                "ユーザ拒否(P)"
                                + "_or_"
                                + "registeredIgnoreNum"
                                + "_"
                                + str(self.__IGNORE_PHONE_NUM)
                            )
                            pass
                        else:
                            bot = LINENotifyBot(access_token=self.__LINE_ACCESS_TOKEN)
                            bot.send(
                                message="\n更新時間"
                                + str(datetime.datetime.now())
                                + "\n"
                                + call_arriveORsend
                                + CallLi
                                + "\n",
                                CHANNEL_ID=self.__CHANNEL_ID,
                                image=None,
                            )
        except IndexError:
            print(IndexError)
            return self.ipChange()
        return

    def ipChange(self) -> None:
        try:
            reqTokenGetDisc = self.session.get(
                self.__BASE_URL + self.__MAIN_PATH + self.__SUB_PATH_BASIC_V4PPPOE,
                **self.post_kwargs,
            )
        except MaxRetryError as e:
            pool = getattr(e, "pool", None)  # 元の pool が取れる場合はそれを再利用
            raise MaxRetryError(
                pool=pool,
                url=self.__BASE_URL + self.__MAIN_PATH + self.__SUB_PATH_BASIC_V4PPPOE,
                reason=e.reason,
            ) from e
        except Exception as e:
            if "WinError 10055" in str(e):
                raise MemoryIsOverflow_Exception()
            print("ConnectionError_" + str(e.args))
            time.sleep(60)
            return self.ipChange()
        if not "200" == str(reqTokenGetDisc.status_code):
            print("エラー")
            time.sleep(12)
            return self.ipChange()
        # cookie = self.session.cookies['HGWSESSIONID']
        # cookies = {
        # 	'HGWSESSIONID': cookie
        # }
        soup = BeautifulSoup(reqTokenGetDisc.content, "html.parser")
        # token_element = soup.find('input',{'name':'SECURITY_TOKEN'})['value']
        token_element = soup.find("input", {"name": "SECURITY_TOKEN"}).get("value")
        print(token_element)
        posdata = {"pppoeSessionID": "1", "SECURITY_TOKEN": token_element}
        self.post_kwargs.update(
            data=posdata,
            # cookies=cookies
        )
        disconnect = self.session.post(
            self.__BASE_URL + self.__SUB_PATH_BASIC_V4PPPOE + "disconnect",
            **self.post_kwargs,
        )
        print(str(disconnect.status_code))
        self.post_kwargs.update(
            data=None,
            # cookies=cookies
        )
        connectChk = "None"
        i = 0
        while not '<div id = "STATUS_SESSION1" >未接続</div>' in connectChk:
            try:
                reqTokenGetCon = self.session.get(
                    self.__BASE_URL + self.__SUB_PATH_BASIC_V4PPPOE, **self.post_kwargs
                )
                soup = BeautifulSoup(reqTokenGetCon.content, "html.parser")

                # token_element = soup.find('input',{'name':'SECURITY_TOKEN'})['value']
                # token_element = soup.find("input", {"name": "SECURITY_TOKEN"}).get(
                #     "value"
                # )
                token_element = soup.find("input", {"name": "SECURITY_TOKEN"})
                if token_element is None:
                    raise token_err()
                token_element = token_element.get("value")
                print(token_element)
                posdata = {"pppoeSessionID": "1", "SECURITY_TOKEN": token_element}
                self.post_kwargs.update(
                    data=posdata,
                    # cookies=cookies
                )
                connect = self.session.post(
                    self.__BASE_URL + self.__SUB_PATH_BASIC_V4PPPOE + "connect",
                    **self.post_kwargs,
                )
                print(str(connect.status_code))
                connectChk = connect.text
            except Exception as e:
                if "WinError 10055" in str(e):
                    raise MemoryIsOverflow_Exception()
                self.post_kwargs.update(
                    data=None,
                    # cookies=cookies
                )
                print("ConnectionError_" + str(e.args))
                if "None" in str(e):
                    pass
                else:
                    i += 1
                if i == 60:
                    sys.exit()
                time.sleep(60)
                pass
