import re
import time
import random

from dslclib import (
    ExpressionController,
    ExpressionType,
    MotionType,
    BodyController,
    FaceRecognitionClient,
    EmotionType,
    Text2SpeechClient,
)

class RobotBodyController(object):
    def __init__(self, ip: str | None = None) -> None:
        self.body: BodyController = BodyController(ip=ip)
        pass

    def __call__(self, key):
        # ここにmotionを追加していく
        if key == "greeting" or key == 'お辞儀': # お辞儀: greeting
            self.playMotion(MotionType.Greeting)
        elif key == "nod" or key == "うなずく": # うなずく: nodding
            self.playMotion(MotionType.Nod)
        elif key == "nod_deep" or key == "深くうなずく":    # 深くうなずく: nodding deeply
            self.playMotion(MotionType.NodDeep)
        elif key == "nono" or key == "首を横に振る":  # 首を横に振る: shaking head
            self.playMotion(MotionType.Nono)
        elif key == "lbp":
            self.playMotion(MotionType.LeftHandBasePositin)
        elif key == "rbp":
            self.playMotion(MotionType.RightHandBasePosition)
        elif key == "rhp":
            self.body.play_motion("right_hand_palmup")
        elif key == "lhp":
            self.body.play_motion("left_hand_palmup")
        elif key == "lhm":
            self.body.play_motion("left_hand_me")
            time.sleep(1.0)
            self.body.play_motion(MotionType.LeftHandBasePositin)
        elif key == "rhm":
            self.body.play_motion("right_hand_me")
            time.sleep(1.0)
            self.body.play_motion(MotionType.RightHandBasePosition)
        elif key == "lhy":
            self.body.play_motion("left_hand_you")
        # elif key == "":
        #     self.body.play_motion()
        elif key == "setgazedown":
            self.body.play_motion("greeting_deep_head")
            self.body.play_motion("greeting_deep_eye")
        elif key == "positivemove":
            rcommand = [
                "right_hand_beatstroke_palmside",
                "right_hand_beatstroke_palmup",
                "left_hand_beatstroke_palmside",
                "left_hand_beatstroke_palmup"
            ]
            random.shuffle(rcommand)
            self.body.play_motion(rcommand[0])
            time.sleep(1.0)
            self.body.play_motion(MotionType.RightHandBasePosition)
            self.body.play_motion(MotionType.LeftHandBasePositin)
        elif key == "thinking" or key == "悩む": # 悩む: thinking
            self.body.play_motion("right_hand_grasp_mouth")
            self.body.play_motion("greeting_deep_head")
            self.body.play_motion("greeting_deep_eye")
            time.sleep(1.0)
            self.body.play_motion(MotionType.RightHandBasePosition)
        elif key == "surprise":
            self.body.play_motion("call_smartphone")
            time.sleep(1.0)
            self.body.play_motion(MotionType.RightHandBasePosition)
            self.body.play_motion(MotionType.LeftHandBasePositin)
        
    def playMotion(self, motion):
        self.body.play_motion(motion)

    # def setGaze(self, type=["eye", "head"], x=0.0, y=1.2, z=1.5):
    #     # 正面方向:z軸，右方向:x軸，上方向:y軸
    #     # (例)
    #     #   正面に向く: (0.0, 1.2, 1.5)
    #     #   右に向く:   (1.0, 1.2, 1.5)
    #     #   左に向く:   (-1.0, 1.2, 1.5)
    #     if type == ["eye", "head"]:
    #         self.body.gaze(direction=(x, y, z))
    #     elif "eye" in type:
    #         self.body.gaze(eye=(x, y, z))
    #     elif "head":
    #         self.body.gaze(head=(x, y, z))

class RobotExpressionController(object):
    def __init__(self, ip: str | None = None) -> None:
        self.express: ExpressionController = ExpressionController(ip=ip)
        pass

    def __call__(self, key):
        #（済）ここに感情を追加していく
        if key == "a":
            self.setExpression(ExpressionType.MouthA)
        elif key == "i":
            self.setExpression(ExpressionType.MouthI)
        elif key == "u":
            self.setExpression(ExpressionType.MouthU)
        elif key == "e":
            self.setExpression(ExpressionType.MouthE)
        elif key == "o":
            self.setExpression(ExpressionType.MouthO)
        elif key == "n":
            self.setExpression(ExpressionType.Normal)
        elif key == "fs" or key == "喜び" or key == "期待":  # 喜び: happy, 期待: hope
            self.setExpression(ExpressionType.FullSmile)
        elif key == "s" or key == "平常" or key == "信頼":  # 平常: neutral, 信頼: trust
            self.setExpression(ExpressionType.Smile)
        elif key == "b" or key == "悲しみ":  # 悲しみ: sadness
            self.setExpression(ExpressionType.Bad)
        elif key == "an" or key == "怒り": # 怒り: anger
            self.setExpression(ExpressionType.Angry)
        elif key == "ec" or key == "嫌悪": # 嫌悪: disgust
            self.setExpression(ExpressionType.EyeClose)
        elif key == "eo" or key == "驚き":  # 驚き: surprise
            self.setExpression(ExpressionType.EyeOpen)
        elif key == "eu":
            self.setExpression(ExpressionType.EyeUp)
        elif key == "ed" or key == "恐れ": # 恐れ: fear
            self.setExpression(ExpressionType.EyeDown)

    def setExpression(self, emotion):
        self.express.express(emotion)

class CorrespondUserExpression(RobotExpressionController):
    '''
    Basicaly mirroring, partly a facial expression that corresponds to the other person's facial expression.
    For example, if you get angry when the other person is angry and you get angry too, you will get into a fight, so this is an awkward expression. Etc.
    '''
    # def __init__(self):
    #     super().__init__()
    #     self.rec_emo_to_exp_emo = {
    #         'angry': ExpressionType.EyeDown,
    #         'disgust': ExpressionType.Bad,
    #         EmotionType.Fear: ExpressionType.Bad,
    #         EmotionType.Happiness: ExpressionType.FullSmile,
    #         EmotionType.Sadness: ExpressionType.EyeDown,
    #         EmotionType.Surprise: ExpressionType.EyeOpen
    #     }
    def face_recognition(self, threshold):
        rec_client = FaceRecognitionClient()
        output = rec_client.listen(FaceRecognitionClient.summarize_times)
        if (
            output.emotion_score >= threshold 
            and output.emotion == 'happy'
            ):
            return 
        else:
            return None

    def mirror_user_expression(self):
        self.setExpression(self.face_recognition(threshold=0.85))


class RobotSpeechController(object):
    def __init__(self, ip: str | None = None) -> None:
        self.tts: Text2SpeechClient = Text2SpeechClient(ip=ip)
    
    def robotSpeech(self, sentence="", emotion="平常", add_volume=0, add_speed=0, add_pitch=0):
        '''
        When returning from normal to happy, there is a severe drop in pitch and I want to change it
        Want to keep high emotional pitch within normal +5
        Below is worth a little more experimentation
        '''
        emotion_to_voice = {
            '喜び': (125, 200, 120), # 喜び: happy, default pitch=125 
            '悲しみ': (120, 100, 105), # 悲しみ: sadness, default pitch=105
            '期待': (120, 150, 117), # 期待: hope
            '驚き': (125, 250, 115), # 驚き: surprise
            '怒り': (120, 230, 100), # 怒り: angry, default pitch=100
            '恐れ': (125, 250, 115), # 恐れ: fear
            '嫌悪': (120, 100, 95), # 嫌悪: disgust, default pitch=95
            '信頼': (120, 100, 117), # 信頼: trust, default pitch=120
            '平常': (120, 100, 115), # 平常: neutral
        }
        speed, volume, pitch = emotion_to_voice[emotion]
        self.tts.speech(sentence, speed=speed+add_speed, volume=volume+add_volume, pitch=pitch+add_pitch, wait_queue=True, max_num_queue=500)

if __name__ == '__main__':
    module = RobotBodyController()
    # module('a')
    # module('喜び') # 喜び: happy
    # module('嫌悪') # 嫌悪: disgust
    module("悩む") # 悩む: thinking
    
    while(True):
        pass