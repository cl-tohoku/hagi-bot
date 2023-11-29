::setlocal enabledelayedexpansion
::@echo off
::rem 環境変数ProgramFilesで示されるフォルダーよりサブフォルダーも含めてMSVCR*.DLLを検索する

title AmazonPollyServer

powershell "java '-jar'  AmazonPollyServer-jar-with-dependencies.jar | tee log.txt"

::pause