::setlocal enabledelayedexpansion
::@echo off
::rem ���ϐ�ProgramFiles�Ŏ������t�H���_�[���T�u�t�H���_�[���܂߂�MSVCR*.DLL����������

title AmazonPollyServer

powershell "java '-jar'  AmazonPollyServer-jar-with-dependencies.jar | tee log.txt"

::pause