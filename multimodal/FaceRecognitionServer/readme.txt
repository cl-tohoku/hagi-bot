[�T�v]
���̃v���O�����̓J�����摜���͂̊�F���ƁA�F���f�[�^�̃X�g���[�~���O(TCP/IP)���s���܂��B

[�����[�X�m�[�g]
2023/07/05�@��̌����E���ʁE�N��F���@�\��ǉ�
2023/06/07�@�\�t�g�E�F�A�z�z�p�����[�X

[���s��]
Windows10�`
Python3.9�`

[����]
pip install -r requirement.txt

[���s]
�E���s���@
�@run.bat�����s
�E���s����
�@-d �J�����f�o�C�XID���w��B�f�t�H���g��0
�@-p �T�[�o�̃|�[�g�ԍ����w��B�f�t�H���g��4500
�@-di deepface�̔F���C���^�[�o���̎w��(sec)�B-1���w�肷���deepface�F�����s��Ȃ��B�f�t�H���g��5
�E�I�����@
�@�摜�\���E�B���h�E���A�N�e�B�u�ɂ�����Ԃ�Esc�L�[


[�F���f�[�^]
�F���f�[�^�͈ȉ��̓��e���܂݂܂��B
�E�\��
�E��̌���(pitch, roll, yaw)
�E�N��
�E����

[�F���f�[�^(�X�g���[�~���O)]
TCP/IP�N���C�A���g�Ƃ��ăT�[�o�ɐڑ�����ƁA���L�̂悤��Json�f�[�^���T�[�o���瑗�M����܂��B
{"timestamp": 1688538712.4629924, "emotion_class": "neutral", "emotion_score": 0.6734067797660828, "rotation": {"pitch": 0.6194981801431012, "roll": -9.570775799382096, "yaw": -2.8118400203755725}, "age": 28, "gender_class": "Man", "gender_score": 99.167001247406}
�f�[�^�͉��s(\n)��؂�ő��M����܂��B��M���ł͉��s��؂�Ńp�[�X���Ă��������B

[�F���f�[�^(�\��)]
emotion�̕��ނ́Aneutral, happy, surprise, sad, angry, disgust, fear��7�ł��B
�ڍׂɂ��ẮA�g�p���Ă���\��F�����C�u����pypaz(https://github.com/oarriaga/paz)���Q�Ƃ��Ă��������B

[�F���f�[�^(��̌���)]
��̌�����mediapipe(https://github.com/google/mediapipe)�ɂ���ĔF�����ꂽfacemesh�̏������ɐ��肳��܂��B
pitch, roll, yaw�̃f�[�^�͂��ꂼ��p�x�ŏo�͂���܂��B

[�F���f�[�^(�N��E����)]
�N��E���ʂ̔F���ɂ�deepface(https://github.com/serengil/deepface)���g�p���܂��B
����N�����ɂ͔N��E���ʂ̔F�����f��(���ꂼ���500MB)���_�E�����[�h����܂��B
�N��E���ʔF���͖��t���[���s�������ł͂Ȃ����߁A-di�I�v�V�����Ŏw�肵�����b�����ƂɔF���������s���܂��B
�X�g���[�~���O�f�[�^�ɂ��w��b���Ɉ�x�����N��E���ʃf�[�^���܂܂�܂��B


[���l]
���̃v���O�����̓J�������Ɉ�l�̐l�����f���ʂ�z�肵�Ă��܂��B
�����̊炪�J�����摜���ɑ��݂���ꍇ�́A�ł��傫���f������݂̂�F���ΏۂƂ��܂��B
