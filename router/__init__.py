# !/usr/bin/env python3
# __init__.py
import argparse
import datetime
import os
import time
from typing import List, Optional

from dotenv import load_dotenv

from router.config import load_config
from router.router_client import router_client

load_dotenv()  # .env を読み込む
import sys

if sys.version_info < (3, 13):
    raise ImportError(
        f"You are using an unsupported version of Python. Only Python versions"
    )


def get_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=".env にない場合デフォルトを読み込む")
    parser.add_argument(
        "--ip",
        type=str,
        default=os.getenv("IP", "192.168.1.1"),
        help="router_client IP address",
    )
    parser.add_argument("--id", type=str, default=os.getenv("ID", "user"), help="ID")
    parser.add_argument(
        "--password", type=str, default=os.getenv("PASSWORD", "password"), help="PASSWD"
    )
    parser.add_argument(
        "--token",
        type=str,
        default=os.getenv("LINE_ACCESS_TOKEN", "default-token"),
        help="LINE_ACCESS_TOKEN",
    )
    parser.add_argument(
        "--channelId",
        type=str,
        default=os.getenv("CHANNEL_ID", "channelId"),
        help="チャンネルかグループのID",
    )
    parser.add_argument(
        "--myphonenumber",
        type=str,
        default=os.getenv("__MY_PHONE_NUM", None),
        help="家の電話",
    )
    parser.add_argument(
        "--ignorephonenumber",
        type=str,
        default=os.getenv("__IGNORE_PHONE_NUM", None),
        help="無視したい名前",
    )

    args = parser.parse_args(argv)  # ← ここで argv=None なら sys.argv[1:] が使われる
    args.myphonenumber = args.myphonenumber or load_config(args.ip)["__MY_PHONE_NUM"]
    args.ignorephonenumber = (
        args.ignorephonenumber or load_config(args.ip)["__IGNORE_PHONE_NUM"]
    )
    return args


def _real_main(RouterConfig: argparse.Namespace) -> None:
    try:
        inputInterval = int(input("1分以上で指定してください:"))
        if inputInterval <= 0:
            raise ValueError("入力値が0以下です。1分以上で指定してください")
    except ValueError:
        raise ValueError("整数で入力されていません")
    router = router_client(
        IP=RouterConfig.ip,
        ID=RouterConfig.id,
        PASSWD=RouterConfig.password,
        LINE_ACCESS_TOKEN=RouterConfig.token,
        CHANNEL_ID=RouterConfig.channelId,
        MY_PHONE_NUM=RouterConfig.myphonenumber,
        IGNORE_PHONENUM=RouterConfig.ignorephonenumber,
    )

    loop = [0]
    for i in loop:
        loop.append(i + 1)
        router.callHistory()
        print("LOOP_START_" + str(datetime.datetime.now()))
        print(str(i) + "#ループ回数")  # ループ回数
        print(str(inputInterval) + " min waiting...")
        time.sleep(inputInterval * 60)


def main(argv: Optional[List[str]] = None) -> None:
    args: argparse.Namespace = get_args(argv)  # 明示的に渡さなくてもよいが記載
    _real_main(args)
