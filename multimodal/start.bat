@echo off
cd /d %~dp0

echo AmazonPollyServer���N�����܂��B
pushd AmazonPollyServer
start 00-launch-AmazonPollyServer.bat
popd
echo AmazonPollyServer���N�����܂����B
pause
echo

echo Voicemeeter Banana���N�����܂��B
pushd "C:\Program Files (x86)\VB\Voicemeeter"
start voicemeeterpro.exe
popd
echo Voicemeeter Banana���N�����܂����B
echo ���`�󐶐��̂��߁AVoicemeeter Banana�E�B���h�E�E���A1�������āA�K��f�o�C�X���w�肵�Ă��������B
echo �f�o�C�X�̎w�肪����������A�����̃L�[�������Đi��ł��������B
pause > nul
echo

echo �����āA���`�󐶐��̂��߁A�R���g���[���p�l���́u�T�E���h�v���u�Đ��v�^�u��Voicemeeterinput���u�K��̃f�o�C�X�v�ɁA�u�^���v�^�u��VoicemeeterOutput���u�K��̃f�o�C�X�v�ɐݒ肵�܂��B
echo �R���g���[���p�l�����N�����܂��B
timeout 1 > nul
start control mmsys.cpl
echo ��́u�Đ��v�^�u��Voicemeeterinput���u�K��̃f�o�C�X�v�A�u�^���v�^�u��VoicemeeterOutput���u�K��̃f�o�C�X�v�ɐݒ肪�ł�����A�����̃L�[�������Đi��ł��������B
pause
echo

echo CGErica���N�����܂��B
echo     OculusLipSync���N�����܂��B
pushd CGEricaSet\01-OculusLipSync
start OculusLipSyncServer.exe
popd
pause
echo

echo     CGErica���N�����܂��B
pushd CGEricaSet\02-CGErica
start CGErica.exe
popd
pause
echo

echo     MiracleErica���N�����܂��B
pushd CGEricaSet\03-MiracleErica\launcherset
start Erica@CG.bat
popd
pause
echo

echo     JointMapper���N�����܂��B
pushd CGEricaSet\04-JointMapper
start run-Erica.bat
popd
echo CGErica���N�����܂����B
pause
echo

echo FaceRecognitionServer���N�����܂��B
pushd FaceRecognitionServer
start run.bat
popd
echo FaceRecognitionServer���N�����܂����B
echo

echo TCPSocketBridge2���N�����܂��B
pushd WebSocketBridge2
start Launcher2-TCPServer.bat
popd
echo TCPSocketBridge2���N�����܂����B
echo

echo Google Speech API���N�����܂��Bconnect�{�^���������āA�\�P�b�g�ʐM���J�n���Ă��������B
start chrome https://hil-erica.github.io/GoogleSpeechAPI/speech_recognition.html
echo �ݒ肪�ł�����A�����̃L�[�������ăZ�b�g�A�b�v���������Ă��������B
pause > nul
echo

echo ����ł��ׂĂ̕K�v�ȃ\�t�g�E�F�A�������オ��܂����B����őΘb�V�X�e�����J�n���邱�Ƃ��ł��܂��B
echo ����ꂳ�܂ł���!

cmd /k