# Call history from Router
これはなに?

NTT系ルータ PR-500mi,PR-500kiから取得した発着信履歴を元にLineへ送信(通知)する。

## 必須
LINE Notify API

## 実行方法

Router.batを実行

echo int(INPUT_MIN_RELOAD_INTERVAL) | python "%UserProfile%\router\Router.py" "USER" "PASS" "IP" "LINE_TOKEN" "PHONE_NUM" "IGNORE_PHONENUM"

INPUT_MIN_RELOAD_INTERVAL 半角数字 更新時間をパイプ入力
USER                      ベーシック認証時のUserID
PASS                      ベーシック認証時のPassword
IP                        192.168.1.1など
LINE_TOKEN                LINE Notify API
PHONE_NUM                 家の固定電話 市外局番から
IGNORE_PHONENUM           発着信を無視する電話番号子コンマ","で複数対応

## イメージ
![image](https://gitimagefolder.s3.ap-northeast-1.amazonaws.com/LineNotify/Line.png)
![image](https://gitimagefolder.s3.ap-northeast-1.amazonaws.com/LineNotify/cui.png)
