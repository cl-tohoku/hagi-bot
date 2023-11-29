@echo off
cd /d %~dp0

echo これから、貸与式ソフトウェア以外に必要なソフトウェアのインストールを行います。
echo ただし、インストール済みのものはインストールをスキップします。
echo #### 注意！ ####
echo - ソフトウェアがインストールされていないと判断された場合、自動的にソフトウェアのダウンロードとインストールが行われます。
echo - 時どきほかのウィンドウの背面にインストーラが隠れる場合があります。その場合はウィンドウを探してください。
echo - Voicemeeterのインストールのチェックには、デフォルトでのインストール先を探します。もし、既にインストール済みで、"C:\Program Files (x86)\VB\Voicemeeter\voicemeeterpro.exe"以外においてある場合は、処理に気を付けてこのinstaller.batを使用してください。
echo #### 注意！ ####
echo 上記の注意点を理解したら、何かのキーを押して、インストールを始めてください。
pause > nul

where /Q java && echo Javaはインストールされています。
where /Q java || echo Javaがインストールされていません。`https://www.java.com/ja/download/windows_manual.jsp`からWindows オフライン (64ビット)をインストールします。 && powershell -Command "wget https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248242_ce59cff5c23f4e2eaf4e778a117d4c5b -OutFile ./jre-installer.exe" && call jre-installer.exe && del /f jre-installer.exe && echo インストールが完了しました。
where /Q "C:\Program Files (x86)\VB\Voicemeeter:voicemeeterpro.exe" && echo VoicemeeterBananaはインストールされています。
where /Q "C:\Program Files (x86)\VB\Voicemeeter:voicemeeterpro.exe" || echo VoicemeeterBananaがインストールされていません。`https://vb-audio.com/Voicemeeter/banana.htm`からインストールします。 && powershell -Command "wget https://download.vb-audio.com/Download_CABLE/VoicemeeterProSetup.exe -OutFile ./VoicemeeterProsetup.exe" && call VoicemeeterProSetup.exe && del /f VoicemeeterProSetup.exe && echo インストールが完了しました。

echo .aws\credentialsの設定がまだの場合、設定を行ってください。
call AmazonPollyServer/docs/OpenCredentialsDirectory.bat
pause

where /Q python && echo Pythonはインストールされています。 && python -V
where /Q python || echo Pythonがインストールされていません。 && powershell -Command "wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile ./python-3.10.11-amd64.exe" && call python-3.10.11-amd64.exe && del /f python-3.10.11-amd64.exe && echo インストールが完了しました。

where /Q docker && echo Docker for Windowsはインストールされています。
where /Q docker || echo Docker for Windowsがインストールされていません。`https://docs.docker.com/desktop/install/windows-install/`からインストールします。必ずWSL2バックエンドを有効化してください。ブラウザを開きます。 && start chrome https://docs.docker.com/desktop/install/windows-install/ && echo Docker Desktop Installer.exeがダウンロードされたら、この.exeファイルを開き、インストールを完了してください。 && echo インストールが完了したら何かキーを押してください。 && pause > nul && where /Q docker && echo インストールが完了しました。

cmd /k