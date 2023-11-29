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
        if key == "greeting" or key == 'お辞儀':
            self.playMotion(MotionType.Greeting)
        elif key == "nod" or key == "うなずく":
            self.playMotion(MotionType.Nod)
        elif key == "nod_deep" or key == "深くうなずく":
            self.playMotion(MotionType.NodDeep)
        elif key == "nono" or key == "首を横に振る":
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
        elif key == "thinking" or key == "悩む":
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
        elif key == "fs" or key == "喜び" or key == "期待":
            self.setExpression(ExpressionType.FullSmile)
        elif key == "s" or key == "平常" or key == "信頼":
            self.setExpression(ExpressionType.Smile)
        elif key == "b" or key == "悲しみ":
            self.setExpression(ExpressionType.Bad)
        elif key == "an" or key == "怒り":
            self.setExpression(ExpressionType.Angry)
        elif key == "ec" or key == "嫌悪":
            self.setExpression(ExpressionType.EyeClose)
        elif key == "eo" or key == "驚き":
            self.setExpression(ExpressionType.EyeOpen)
        elif key == "eu":
            self.setExpression(ExpressionType.EyeUp)
        elif key == "ed" or key == "恐れ":
            self.setExpression(ExpressionType.EyeDown)

    def setExpression(self, emotion):
        self.express.express(emotion)

class CorrespondUserExpression(RobotExpressionController):
    '''
    基本ミラーで、一部相手の表情に対応する表情
    例えば、相手が怒っている時に自分も怒ったら喧嘩になるので、こちらは気まずい表情。など
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
        平常から喜んだあと戻る時、ピッチの落差が激しいので、変えたいという気持ち
        高い感情のピッチを平常+5以内に収めたい
        下はもう少し試してみる価値あり
        '''
        emotion_to_voice = {
            '喜び': (125, 200, 120), # 元pitch=125
            '悲しみ': (120, 100, 105), # 元pitch=105
            '期待': (120, 150, 117), 
            '驚き': (125, 250, 115), 
            '怒り': (120, 230, 100), # 元pitch=100
            '恐れ': (125, 250, 115), 
            '嫌悪': (120, 100, 95), # 元pitch=95
            '信頼': (120, 100, 117), # 元pitch=120
            '平常': (120, 100, 115),
        }
        speed, volume, pitch = emotion_to_voice[emotion]
        self.tts.speech(sentence, speed=speed+add_speed, volume=volume+add_volume, pitch=pitch+add_pitch, wait_queue=True, max_num_queue=500)

if __name__ == '__main__':
    module = RobotBodyController()
    # module('a')
    # module('喜び')
    # module('嫌悪')
    module("悩む")
    
    while(True):
        pass