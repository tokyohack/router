@echo off
title Router && cd "%UserProfile%"
if not exist CALL_HIS_PATH.txt ( copy nul CALL_HIS_PATH.txt )
echo int(INPUT_MIN_RELOAD_INTERVAL) | python "%UserProfile%\router\Router.py" "USER" "PASS" "IP" "LINE_TOKEN" "CHANNEL_ID" "PHONE_NUM" "IGNORE_PHONENUM"
pause
