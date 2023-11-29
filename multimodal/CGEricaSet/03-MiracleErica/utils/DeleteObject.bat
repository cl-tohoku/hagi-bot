::if not "%~0"=="%~dp0.\%~nx0" (
::    start /min cmd /c,"%~dp0.\%~nx0" %*
::    exit
::)

set executecommand=java -jar JTCPClient.jar
set hostName=127.0.0.1
set portNum=21000
::\n, \sp, \t
set command=deleteobject={\"id\":\"sampleobject\"}\n

%executecommand% %hostName% %portNum% "%command%"

::pause