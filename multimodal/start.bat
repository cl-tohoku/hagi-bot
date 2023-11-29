@echo off
cd /d %~dp0

echo AmazonPollyServerを起動します。
pushd AmazonPollyServer
start 00-launch-AmazonPollyServer.bat
popd
echo AmazonPollyServerが起動しました。
pause
echo

echo Voicemeeter Bananaを起動します。
pushd "C:\Program Files (x86)\VB\Voicemeeter"
start voicemeeterpro.exe
popd
echo Voicemeeter Bananaが起動しました。
echo 口形状生成のため、Voicemeeter Bananaウィンドウ右上のA1を押して、規定デバイスを指定してください。
echo デバイスの指定が完了したら、何かのキーを押して進んでください。
pause > nul
echo

echo 続いて、口形状生成のため、コントロールパネルの「サウンド」→「再生」タブでVoicemeeterinputを「規定のデバイス」に、「録音」タブでVoicemeeterOutputを「規定のデバイス」に設定します。
echo コントロールパネルを起動します。
timeout 1 > nul
start control mmsys.cpl
echo 上の「再生」タブでVoicemeeterinputを「規定のデバイス」、「録音」タブでVoicemeeterOutputを「規定のデバイス」に設定ができたら、何かのキーを押して進んでください。
pause
echo

echo CGEricaを起動します。
echo     OculusLipSyncを起動します。
pushd CGEricaSet\01-OculusLipSync
start OculusLipSyncServer.exe
popd
pause
echo

echo     CGEricaを起動します。
pushd CGEricaSet\02-CGErica
start CGErica.exe
popd
pause
echo

echo     MiracleEricaを起動します。
pushd CGEricaSet\03-MiracleErica\launcherset
start Erica@CG.bat
popd
pause
echo

echo     JointMapperを起動します。
pushd CGEricaSet\04-JointMapper
start run-Erica.bat
popd
echo CGEricaが起動しました。
pause
echo

echo FaceRecognitionServerを起動します。
pushd FaceRecognitionServer
start run.bat
popd
echo FaceRecognitionServerが起動しました。
echo

echo TCPSocketBridge2を起動します。
pushd WebSocketBridge2
start Launcher2-TCPServer.bat
popd
echo TCPSocketBridge2が起動しました。
echo

echo Google Speech APIを起動します。connectボタンを押して、ソケット通信を開始してください。
start chrome https://hil-erica.github.io/GoogleSpeechAPI/speech_recognition.html
echo 設定ができたら、何かのキーを押してセットアップを完了してください。
pause > nul
echo

echo これですべての必要なソフトウェアが立ち上がりました。これで対話システムを開始することができます。
echo お疲れさまでした!

cmd /k