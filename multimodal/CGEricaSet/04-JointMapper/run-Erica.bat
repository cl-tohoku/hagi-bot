setlocal enabledelayedexpansion
::@echo off
rem 環境変数ProgramFilesで示されるフォルダーよりサブフォルダーも含めてMSVCR*.DLLを検索する

title JointMapperPlusUltraSuperFaceConsole

set externalPath=./lib/
set externalJars=
for /r "%externalPath%" %%A in (*.jar) do (
	set externalJars=!externalJars!%%A;
)
echo %externalJars%
::pause

::https://detail.chiebukuro.yahoo.co.jp/qa/question_detail/q1092589030
::http://www.yamatyuu.net/computer/program/bat/for_files.html

java -jar JointMapperPlusUltraSuperFace.jar config\EricaCG EricaCG

::pause