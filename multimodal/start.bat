@echo off
cd /d %~dp0

echo AmazonPollyServer will be launched.
pushd AmazonPollyServer
start 00-launch-AmazonPollyServer.bat
popd
echo AmazonPollyServer has been launched.
pause
echo

echo Voicemeeter Banana will be launched.
pushd "C:\Program Files (x86)\VB\Voicemeeter"
start voicemeeterpro.exe
popd
echo Voicemeeter Banana has been launched.
echo Press A1 at the top right of the Voicemeeter Banana window and specify the default device for mouth shape generation.
echo Once the device is specified, press any key to continue.
pause > nul
echo

echo Next, for mouth shape generation, set Voicemeeterinput as the "default device" in the "Playback" tab and VoicemeeterOutput as the "default device" in the "Recording" tab of the control panel's "Sound".
echo The control panel will be launched.
timeout 1 > nul
start control mmsys.cpl
echo After setting Voicemeeterinput as the "default device" in the "Playback" tab and VoicemeeterOutput as the "default device" in the "Recording" tab, press any key to continue.
pause
echo

echo CGErica will be launched.
echo     OculusLipSync will be launched.
pushd CGEricaSet\01-OculusLipSync
start OculusLipSyncServer.exe
popd
pause
echo

echo     CGErica will be launched.
pushd CGEricaSet\02-CGErica
start CGErica.exe
popd
pause
echo

echo     MiracleErica will be launched.
pushd CGEricaSet\03-MiracleErica\launcherset
start Erica@CG.bat
popd
pause
echo

echo     JointMapper will be launched.
pushd CGEricaSet\04-JointMapper
start run-Erica.bat
popd
echo CGErica has been launched.
pause
echo

echo FaceRecognitionServer will be launched.
pushd FaceRecognitionServer
start run.bat
popd
echo FaceRecognitionServer has been launched.
echo

echo TCPSocketBridge2 will be launched.
pushd WebSocketBridge2
start Launcher2-TCPServer.bat
popd
echo TCPSocketBridge2 has been launched.
echo

echo Google Speech API will be launched. Press connect to start socket communication.
start chrome https://hil-erica.github.io/GoogleSpeechAPI/speech_recognition.html
echo Once the setup is complete, press any key to finish.
pause > nul
echo

echo All necessary software has been launched. You can now start the dialogue system.
echo Well done!

cmd /k