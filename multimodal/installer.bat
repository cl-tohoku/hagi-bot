@echo off
cd /d %~dp0

echo ���ꂩ��A�ݗ^���\�t�g�E�F�A�ȊO�ɕK�v�ȃ\�t�g�E�F�A�̃C���X�g�[�����s���܂��B
echo �������A�C���X�g�[���ς݂̂��̂̓C���X�g�[�����X�L�b�v���܂��B
echo #### ���ӁI ####
echo - �\�t�g�E�F�A���C���X�g�[������Ă��Ȃ��Ɣ��f���ꂽ�ꍇ�A�����I�Ƀ\�t�g�E�F�A�̃_�E�����[�h�ƃC���X�g�[�����s���܂��B
echo - ���ǂ��ق��̃E�B���h�E�̔w�ʂɃC���X�g�[�����B���ꍇ������܂��B���̏ꍇ�̓E�B���h�E��T���Ă��������B
echo - Voicemeeter�̃C���X�g�[���̃`�F�b�N�ɂ́A�f�t�H���g�ł̃C���X�g�[�����T���܂��B�����A���ɃC���X�g�[���ς݂ŁA"C:\Program Files (x86)\VB\Voicemeeter\voicemeeterpro.exe"�ȊO�ɂ����Ă���ꍇ�́A�����ɋC��t���Ă���installer.bat���g�p���Ă��������B
echo #### ���ӁI ####
echo ��L�̒��ӓ_�𗝉�������A�����̃L�[�������āA�C���X�g�[�����n�߂Ă��������B
pause > nul

where /Q java && echo Java�̓C���X�g�[������Ă��܂��B
where /Q java || echo Java���C���X�g�[������Ă��܂���B`https://www.java.com/ja/download/windows_manual.jsp`����Windows �I�t���C�� (64�r�b�g)���C���X�g�[�����܂��B && powershell -Command "wget https://javadl.oracle.com/webapps/download/AutoDL?BundleId=248242_ce59cff5c23f4e2eaf4e778a117d4c5b -OutFile ./jre-installer.exe" && call jre-installer.exe && del /f jre-installer.exe && echo �C���X�g�[�����������܂����B
where /Q "C:\Program Files (x86)\VB\Voicemeeter:voicemeeterpro.exe" && echo VoicemeeterBanana�̓C���X�g�[������Ă��܂��B
where /Q "C:\Program Files (x86)\VB\Voicemeeter:voicemeeterpro.exe" || echo VoicemeeterBanana���C���X�g�[������Ă��܂���B`https://vb-audio.com/Voicemeeter/banana.htm`����C���X�g�[�����܂��B && powershell -Command "wget https://download.vb-audio.com/Download_CABLE/VoicemeeterProSetup.exe -OutFile ./VoicemeeterProsetup.exe" && call VoicemeeterProSetup.exe && del /f VoicemeeterProSetup.exe && echo �C���X�g�[�����������܂����B

echo .aws\credentials�̐ݒ肪�܂��̏ꍇ�A�ݒ���s���Ă��������B
call AmazonPollyServer/docs/OpenCredentialsDirectory.bat
pause

where /Q python && echo Python�̓C���X�g�[������Ă��܂��B && python -V
where /Q python || echo Python���C���X�g�[������Ă��܂���B && powershell -Command "wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe -OutFile ./python-3.10.11-amd64.exe" && call python-3.10.11-amd64.exe && del /f python-3.10.11-amd64.exe && echo �C���X�g�[�����������܂����B

where /Q docker && echo Docker for Windows�̓C���X�g�[������Ă��܂��B
where /Q docker || echo Docker for Windows���C���X�g�[������Ă��܂���B`https://docs.docker.com/desktop/install/windows-install/`����C���X�g�[�����܂��B�K��WSL2�o�b�N�G���h��L�������Ă��������B�u���E�U���J���܂��B && start chrome https://docs.docker.com/desktop/install/windows-install/ && echo Docker Desktop Installer.exe���_�E�����[�h���ꂽ��A����.exe�t�@�C�����J���A�C���X�g�[�����������Ă��������B && echo �C���X�g�[�������������牽���L�[�������Ă��������B && pause > nul && where /Q docker && echo �C���X�g�[�����������܂����B

cmd /k