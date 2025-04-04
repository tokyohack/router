# !/usr/bin/env python3
# config.py
import configparser
import random

# 設定読み込み


def load_config(ip: str) -> dict[str, str]:
    config = configparser.ConfigParser()
    config.optionxform = str  # ★キー名をそのまま保持する ループで取得すると小文字になるため、キー名を小文字に変換しない
    config.read(r"../config.ini", encoding="utf8")
    settings = {key: value for key, value in config["settings"].items()}
    settings["__BASE_URL"] = settings["__BASE_URL"].format(ip=ip)
    settings["__CALL_HISTORY_URL"] = (
        settings["__BASE_URL"] + settings["__MAIN_PATH"] + settings["__CALL_HIS"]
    )
    return settings
    # return {
    #         "__BASE_URL"         : config["settings"]["__BASE_URL"],
    #         "__SUB_PATH_BASIC_V4PPPOE": config["settings"]["__SUB_PATH_BASIC_V4PPPOE"]
    # }


# config_values = load_config("192.168.1.1")
# print(config_values["__BASE_URL"])


# HTTPリクエストのタイムアウト設定
connect_timeout_start = random.randint(12, 24)
connect_timeout_end = random.randint(1, 10)
read_timeout_start = random.randint(24, 30)
read_timeout_end = random.randint(1, 10)

REQUEST_TIMEOUT = (
    float(f"{connect_timeout_start}.{connect_timeout_end}"),
    float(f"{read_timeout_start}.{read_timeout_end}"),
)
