setlocal enabledelayedexpansion
::@echo off
rem ���ϐ�ProgramFiles�Ŏ������t�H���_�[���T�u�t�H���_�[���܂߂�MSVCR*.DLL����������

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