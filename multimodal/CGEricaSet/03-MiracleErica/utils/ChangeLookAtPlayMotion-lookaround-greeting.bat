::if not "%~0"=="%~dp0.\%~nx0" (
::    start /min cmd /c,"%~dp0.\%~nx0" %*
::    exit
::)

set executecommand=java -jar JTCPClient.jar
set hostName=127.0.0.1
set portNum=21000
::\n, \sp, \t

::正面
set command=EyeController={\"id\": \"EyeController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=HeadController={\"id\": \"HeadController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=BodyController={\"id\": \"BodyController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 0.8,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手出す
set command=playmotion=right_hand_palmup2headcontroller\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手下ろす
set command=playmotion=righthandbaseposition\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 1
::お辞儀
set command=playmotion=greeting\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 4

::体ごと右
set command=EyeController={\"id\": \"EyeController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 1.3,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=HeadController={\"id\": \"HeadController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 1.3,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=BodyController={\"id\": \"BodyController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 1.3,\"y\": 0.8,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手出す
set command=playmotion=right_hand_palmup2headcontroller\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手下ろす
set command=playmotion=righthandbaseposition\n
%executecommand% %hostName% %portNum% "%command%"
Timeout 1
::お辞儀
set command=playmotion=greeting\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 4

::顔は左
set command=EyeController={\"id\": \"EyeController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": -1.3,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=HeadController={\"id\": \"HeadController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": -1.3,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手出す
set command=playmotion=right_hand_palmup2headcontroller\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 3
::右手下ろす
set command=playmotion=righthandbaseposition\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 1
::お辞儀
set command=playmotion=greeting\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 4

::正面
set command=EyeController={\"id\": \"EyeController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=HeadController={\"id\": \"HeadController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 1.2,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"
set command=BodyController={\"id\": \"BodyController\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 0.8,\"z\": 1.5},\"translateSpeed\": 2.0}\n
%executecommand% %hostName% %portNum% "%command%"

Timeout 5

::お辞儀
set command=playmotion=greeting\n
%executecommand% %hostName% %portNum% "%command%"

::set command=playmotion=right_hand_you\n
::%executecommand% %hostName% %portNum% "%command%"

::pause