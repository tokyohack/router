# coding: utf-8

import requests, re, datetime, time, random, sys
from bs4 import BeautifulSoup
from line_notify_bot import LINENotifyBot
from ERRCODE import MemoryIsOverflow_Exception,MaxRetryError

loop = [1]

# batから引数を受け取る
ID = sys.argv[1]
PASSWD = sys.argv[2]
IP = sys.argv[3]
LINE_ACCESS_TOKEN = sys.argv[4]
MY_PHONE_NUM = sys.argv[5]
IGNORE_PHONENUM = sys.argv[6]


class Router:
    def __init__(
            self,
            ID,
            PASSWD,
            IP,
            LINE_ACCESS_TOKEN,
            MY_PHONE_NUM,
            IGNORE_PHONENUM=None
    ):

        self.URL = 'http://' + IP + '/ntt/'
        self.URL_BASIC_V4PPPOE = 'basic/v4pppoe/'
        self.CALL_HIS = 'information/callHistory'
        self.LINE_ACCESS_TOKEN = LINE_ACCESS_TOKEN
        self.MY_PHONE_NUM = MY_PHONE_NUM
        self.IGNORE_PHONENUM = IGNORE_PHONENUM
        connectTimeoutSta = random.randint(12, 24)
        connectTimeoutEnd = random.randint(1, 10)
        readTimeoutSta = random.randint(24, 30)
        readTimeoutEnd = random.randint(1, 10)
        reqestsTimeout = (
            float(f'{connectTimeoutSta}.{connectTimeoutEnd}'),
            float(f'{readTimeoutSta}.{readTimeoutEnd}')
        )

        self.session = requests.Session()
        headers = {
            'referer': self.URL,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
        }
        auth = (ID, PASSWD)
        self.post_kwargs = dict(
            headers=headers,
            timeout=reqestsTimeout,
            data=None,
            cookies=None,
            auth=auth
        )

    def callHistory(self):
        CALL_HIS_PATH = r'.//CALL_HIS_PATH.txt'
        with open(CALL_HIS_PATH, mode='r', encoding='utf8') as CALL_HIS_LIS:
            callHisLisOpen = CALL_HIS_LIS.read()
        try:
            called = self.session.get(
                self.URL + self.CALL_HIS,
                **self.post_kwargs
            )
        except Exception as e:
            if 'WinError 10055' in str(e):
                raise MemoryIsOverflow_Exception()
            print('ConnectionError_' + str(e.args))
            time.sleep(2)
            return self.ipChange()
        html = str(called.text)
        try:
            CallLis = html.split('There are 100 entries.\n\n', 1)[1].split('</pre>', 1)[0]
            CallLis = re.sub(r'^.....', '', CallLis)
            CallLis = re.sub(r'\n.....', '\n', CallLis).splitlines()
            for CallLi in CallLis:
                if CallLi in callHisLisOpen:
                    pass
                else:
                    with open(CALL_HIS_PATH, mode='a', encoding='utf8') as f:
                        f.write(CallLi + '\n')
                        if '発信' in CallLi:
                            call_arriveORsend = '【発信】しました。\n'
                            print('発信有り')
                        elif '着信' in CallLi:
                            call_arriveORsend = '【着信】がありました。\n'
                            print('着信有り')
                        else:
                            call_arriveORsend = '宛先不明が不明です。\n'

                        CallLi = re.sub(r' 1 TEL1 - - - -', '', CallLi)
                        CallLi = re.sub(r' - - - - - -', '', CallLi)
                        CallLi = re.sub(r' - - - - 1 TEL1 0 -', '', CallLi)
                        CallLi = re.sub(r' - ', '\n', CallLi)
                        CallLi = re.sub(r' 接続先切断', '\n接続先切断', CallLi)
                        CallLi = re.sub(r' 自切断', '\n自切断', CallLi)
                        CallLi = re.sub(r' 宛先不明', '\n宛先不明', CallLi)
                        CallLi = re.sub(r' ' + self.MY_PHONE_NUM + ' ', '\nhttps://www.google.com/search?q=', CallLi)

                        print('\n更新時間' + str(datetime.datetime.now()) + '\n' + call_arriveORsend + CallLi + '\n')
                        if 'ユーザ拒否(P)' in CallLi or self.IGNORE_PHONENUM in CallLi:
                            print('ユーザ拒否(P)' + '_or_' + 'registeredIgnoreNum' + '_' + self.IGNORE_PHONENUM)
                            pass
                        else:
                            bot = LINENotifyBot(access_token=self.LINE_ACCESS_TOKEN)
                            bot.send(
                                message='\n更新時間' + str(
                                    datetime.datetime.now()) + '\n' + call_arriveORsend + CallLi + '\n'
                            )
        except IndexError:
            CallLis = None
            print(IndexError)
            return self.ipChange()
        return

    def ipChange(self):
        try:
            reqTokenGetDisc = self.session.get(
                self.URL + self.URL_BASIC_V4PPPOE,
                **self.post_kwargs
            )
        except Exception as e:
            if 'WinError 10055' in str(e):
                raise MemoryIsOverflow_Exception()
            print('ConnectionError_' + str(e.args))
            if 'MaxRetryError' in str(e):
                raise MaxRetryError()
            print('ConnectionError_' + str(e.args))
            time.sleep(60)
            return self.ipChange()
        if not '200' == str(reqTokenGetDisc.status_code):
            print('エラー')
            time.sleep(12)
            return self.ipChange()
        # cookie = self.session.cookies['HGWSESSIONID']
        # cookies = {
        # 	'HGWSESSIONID': cookie
        # }
        soup = BeautifulSoup(reqTokenGetDisc.content, 'html.parser')
        # token = soup.find('input',{'name':'SECURITY_TOKEN'})['value']
        token = soup.find('input', {'name': 'SECURITY_TOKEN'}).get('value')
        print(token)
        posdata = {
            'pppoeSessionID': '1',
            'SECURITY_TOKEN': token
        }
        self.post_kwargs.update(
            data=posdata,
            # cookies=cookies
        )
        disconnect = self.session.post(
            self.URL + self.URL_BASIC_V4PPPOE + 'disconnect',
            **self.post_kwargs
        )
        print(str(disconnect.status_code))

        self.post_kwargs.update(
            data=None,
            # cookies=cookies
        )

        connectChk = 'None'
        i = 0
        while not '<div id = "STATUS_SESSION1" >未接続</div>' in connectChk:
            try:
                reqTokenGetCon = self.session.get(
                    self.URL + self.URL_BASIC_V4PPPOE,
                    **self.post_kwargs
                )
                soup = BeautifulSoup(reqTokenGetCon.content, 'html.parser')
                # token = soup.find('input',{'name':'SECURITY_TOKEN'})['value']
                token = soup.find('input', {'name': 'SECURITY_TOKEN'}).get('value')
                print(token)
                posdata = {
                    'pppoeSessionID': '1',
                    'SECURITY_TOKEN': token
                }
                self.post_kwargs.update(
                    data=posdata,
                    # cookies=cookies
                )

                connect = self.session.post(
                    self.URL + self.URL_BASIC_V4PPPOE + 'connect',
                    **self.post_kwargs
                )
                print(str(connect.status_code))
                connectChk = connect.text
            except Exception as e:
                if 'WinError 10055' in str(e):
                    raise MemoryIsOverflow_Exception()
                self.post_kwargs.update(
                    data=None,
                    # cookies=cookies
                )
                print('ConnectionError_' + str(e.args))
                if 'None' in str(e):
                    pass
                else:
                    i += 1
                if i == 60:
                    sys.exit()
                time.sleep(60)
                pass


if __name__ == '__main__':
    try:
        inputInterval = int(input('1分以上で指定してください:'))
        if inputInterval == 0:
            print('0が入力されました、1分以上で指定してください')
            sys.exit()
    except Exception:
        print('整数で入力されていません')
        sys.exit()
    router = Router(ID, PASSWD, IP, LINE_ACCESS_TOKEN, MY_PHONE_NUM, IGNORE_PHONENUM)
    for i in loop:
        loop.append(i + 1)
        router.callHistory()
        print('LOOP_START_' + str(datetime.datetime.now()))
        print(str(i) + '#ループ回数')  # ループ回数
        print(str(inputInterval) + ' min waiting...')
        time.sleep(inputInterval * 60)
