setlocal enabledelayedexpansion
::@echo off

title WebSocketBridge2


set params="websocketport=8000"
set params=!params! "tcpport=8888"
::set params=!params! "tcphost=127.0.0.1"

java -jar WebSocketBridge2Multi.jar %params%
pause