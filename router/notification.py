# !/usr/bin/env python3
# notification.py
import requests


class LINENotifyBot:
    API_URL = "https://api.line.me/v2/bot/message/push"

    def __init__(self, access_token: str) -> None:
        self.__headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {{ {access_token} }}",
        }

    def send(
        self,
        message: str,
        image: str,
        CHANNEL_ID: str,
    ) -> None:
        return self._send(
            _message=message,
            _image=image,
            _CHANNEL_ID=CHANNEL_ID,
        )

    def _send(
        self,
        _message: str,
        _image: str,
        _CHANNEL_ID: str,
    ) -> None:
        payload = {
            "to": _CHANNEL_ID,
            "messages": [{"type": "text", "text": _message}],
        }
        files = {}
        if _image != None:
            files = {"imageFile": open(_image, "rb")}
        response = requests.post(
            LINENotifyBot.API_URL,
            headers=self.__headers,
            # data = json.dumps(payload),
            json=payload,
            # files = files
        )
        print(response.status_code)
        print(response.text)


if __name__ == "__main__":
    try:
        bot: LINENotifyBot = LINENotifyBot(access_token=None)
        bot.send(
            message=None,
            image=None,
            CHANNEL_ID=None,
        )
    except ValueError as e:
        print(e)
