echo off

set targetdir=%USERPROFILE%\.aws
set targetfile=%targetdir%\credentials

IF "%targetdir%" == "" (
	echo ファイルを指定しろよ
) ELSE IF NOT EXIST "%targetdir%" ( 
	mkdir %targetdir%
	echo make %targetdir%
) ELSE (
	echo OK
)

IF "%targetfile%" == "" (
	echo ファイルを指定しろよ
) ELSE IF NOT EXIST "%targetfile%" ( 
	echo [default] >> %targetfile%
	echo aws_access_key_id = *** >> %targetfile%
	echo aws_secret_access_key = *** >> %targetfile% 
) ELSE (
	echo OK
)

explorer %USERPROFILE%\.aws