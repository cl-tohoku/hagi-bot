::if not "%~0"=="%~dp0.\%~nx0" (
::    start /min cmd /c,"%~dp0.\%~nx0" %*
::    exit
::)

set executecommand=java -jar JTCPClient.jar
set hostName=127.0.0.1
set portNum=21000
::\n, \sp, \t
set command=createobject={\"id\":\"sampleobject\",\"scale\":{\"x\":1.0,\"y\":0.1,\"z\":1.0}, \"position\":{\"x\":0.0,\"y\":0.8,\"z\":2.5}, \"rotation\":{\"x\":0,\"y\":0,\"z\":0}, \"color\":{\"r\":128,\"g\":128,\"b\":128,\"a\":128}, \"isLookTarget\":true}\n

%executecommand% %hostName% %portNum% "%command%"

::pause