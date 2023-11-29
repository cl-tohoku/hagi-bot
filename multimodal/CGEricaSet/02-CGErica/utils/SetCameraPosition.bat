::if not "%~0"=="%~dp0.\%~nx0" (
::    start /min cmd /c,"%~dp0.\%~nx0" %*
::    exit
::)

set executecommand=java -jar JTCPClient.jar
set hostName=127.0.0.1
set portNum=9876
::\n, \sp, \t
set command=camera={\"id\": \"Main Camera\",\"motionTowardObject\": \"\",\"targetMotionMode\": 2,\"targetPoint\": {\"x\": 0.0,\"y\": 1.2,\"z\": 2.5},\"translateTime\": 1000, \"targetRotation\": {\"x\":0.0,\"y\": -135.0,\"z\": 0.0},\"rotateTime\": 1000}\n
%executecommand% %hostName% %portNum% "%command%"

::pause