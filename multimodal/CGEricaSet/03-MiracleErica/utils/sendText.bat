if not "%~0"=="%~dp0.\%~nx0" (
    start /min cmd /c,"%~dp0.\%~nx0" %*
    exit
)

set executecommand=java -classpath .;./lib;./bin JTCPClient
set hostName=192.168.11.50
set portNum=9876
::\n, \sp, \t
set command=E\n

%executecommand% %hostName% %portNum% %command%

pause