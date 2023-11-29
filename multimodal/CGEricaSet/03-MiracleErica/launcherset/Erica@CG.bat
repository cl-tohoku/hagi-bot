::if not "%~0"=="%~dp0.\%~nx0" (
::    start /min cmd /c,"%~dp0.\%~nx0" %*
::    exit
::)

cd ..\
start MiracleHuman.exe
Timeout 7

cd .\utils

set executecommand=java -jar JTCPClient.jar
set hostName=127.0.0.1
set portNum=21000
::\n, \sp, \t
set command=createobject={\"id\":\"desk\",\"scale\":{\"x\":1.4,\"y\":0.05,\"z\":0.75}, \"position\":{\"x\":0.2,\"y\":0.7,\"z\":0.7}, \"rotation\":{\"x\":0,\"y\":0,\"z\":0}, \"color\":{\"r\":139,\"g\":69,\"b\":19,\"a\":128}}\n

%executecommand% %hostName% %portNum% "%command%"

set command=createobject={\"id\":\"monitor\",\"scale\":{\"x\":0.65,\"y\":0.4,\"z\":0.05}, \"position\":{\"x\":0.8,\"y\":1.05,\"z\":0.55}, \"rotation\":{\"x\":0,\"y\":-45,\"z\":0}, \"color\":{\"r\":100,\"g\":100,\"b\":100,\"a\":128}, \"isLookTarget\":true}\n

%executecommand% %hostName% %portNum% "%command%"

set command=createobject={\"id\":\"humanhead\",\"scale\":{\"x\":0.25,\"y\":0.3,\"z\":0.2}, \"position\":{\"x\":0.0,\"y\":1.2,\"z\":1.5}, \"rotation\":{\"x\":0,\"y\":-90,\"z\":0}, \"color\":{\"r\":241,\"g\":187,\"b\":147,\"a\":128}}\n

%executecommand% %hostName% %portNum% "%command%"

::hands
set command=playmotion=lefthandbaseposition;righthandbaseposition;\n
%executecommand% %hostName% %portNum% "%command%"

::head, eye
set command=EyeController={\"id\": \"EyeController\",\"motionTowardObject\": \"humanhead\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 0,\"z\": 0},\"translateSpeed\": 2.0,\"translateTime\": -1,\"targetRotation\": {\"x\":0.0,\"y\": 0.0,\"z\": 0.0},\"rotateSpeed\": 270,\"rotateTime\": -1,\"keepTime\": 0,\"mode\": 2,\"gazeTracking\": true,\"tracking\": true,\"priority\": 0,\"isBezierCurvePoint\": false,\"fingerData\": []}\n
%executecommand% %hostName% %portNum% "%command%"
set command=HeadController={\"id\": \"HeadController\",\"motionTowardObject\": \"humanhead\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0,\"y\": 0,\"z\": 0},\"translateSpeed\": 1.5,\"translateTime\": -1,\"targetRotation\": {\"x\":0.0,\"y\": 0.0,\"z\": 0.0},\"rotateSpeed\": 270,\"rotateTime\": -1,\"keepTime\": 0,\"mode\": 2,\"gazeTracking\": true,\"tracking\": true,\"priority\": 0,\"isBezierCurvePoint\": false,\"fingerData\": []}\n
%executecommand% %hostName% %portNum% "%command%"


::pause