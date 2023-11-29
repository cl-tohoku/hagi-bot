from dslclib import (
    SpeechRecognitionClient,
    Text2SpeechClient,
    FaceRecognitionClient,
    ExpressionController,
    BodyController,
    ExpressionType,
    MotionType,
    STTRecognitionType,
)
import random, time

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

# ？のときは True を返す．他のときは None を返す
def is_hatena(sentence):
    if sentence.endswith("？") or sentence.endswith("?"):
        return True
    else:
        return False

# 、のときは True を返す．他のときは None を返す
def is_comma(sentence):
    if sentence.endswith("、"):
        return True
    else:
        return False

# …のときは True を返す．他のときは None を返す
def is_santen(sentence):
    if sentence.endswith("…"):
        return True
    else:
        return False

# ルールベース and GPTトークン 動作定義
def define_motion(robotbodycontroller, sentence, gptemotion="", gptmotion=""):
    # robotbodycontroller = RobotBodyController() # ここで毎回インスタンスを生成していたことが原因っぽい
    done_motion = False

    if is_santen(sentence) or 'うーん' in sentence:
        robotbodycontroller('thinking')
        done_motion = True
                                                                    
    elif any(sentence.startswith(s) for s in ['うん', 'はい', 'なるほど', 'そうだね']):
        robotbodycontroller('nod_deep')
        done_motion = True

    elif any(sentence.startswith(s) for s in ['いいえ', 'いや', 'ううん']):
        robotbodycontroller('nono')
        done_motion = True

    if '私' in sentence or 'わたし' in sentence or '僕' in sentence:
        robotbodycontroller('lhm')
        done_motion = True

    elif any(s in sentence for s in ['貴方', 'あなた', 'ユウキ', 'ゆうき']):
        if not any(y in sentence for y in ['ユウキ、', 'ユウキ。', 'ゆうき、', 'ゆうき。', 'ユウキ！', 'ゆうき！']):
            robotbodycontroller('lhy')
            time.sleep(2)
            robotbodycontroller('lbp')
            done_motion = True

    if is_hatena(sentence) and not any(m in sentence for m in ["マジで？", "まじで？", "マジ？", "まじ？", "円？"]):
        # 確認済み
            if random.random() < 0.2:
                pass
            elif random.random() < 0.5:
                robotbodycontroller('lhp')
                time.sleep(2)
                robotbodycontroller('lbp')
            else:
                robotbodycontroller('rhp')
                time.sleep(2)
                robotbodycontroller('rbp')
            done_motion = True
            
        # 確認済み
    if any(m in sentence for m in ["マジで？", "まじで？", "マジ？", "まじ？", "本当に？", "ほんとに？", "え、"]):
        robotbodycontroller('surprise')
        done_motion = True

    if done_motion == False:
        if gptmotion:
            robotbodycontroller(gptmotion)
            
        elif gptemotion:
            if gptemotion in ['喜び', '期待']:
                robotbodycontroller('positivemove')
            elif gptemotion in ['悲しみ']:
                robotbodycontroller('setgazedown')
            # 確認済み
            elif gptemotion in ['驚き']:
                robotbodycontroller('surprise')
        
        elif random.random() < 0.3:
            random_motion = [
                robotbodycontroller('positivemove'),
                robotbodycontroller('rhm'),
                robotbodycontroller('lhm'),
            ]
            random.shuffle(random_motion)
            random_motion[0]

class SampleModel:
    """SampleModel
    オウム返しをする対話モデルサンプル

    Attributes
    ----------
    sr: SpeechRecognitionClient
    tts: Text2SpeechClient
    face: FaceRecognitionClient
    express: ExpressionController
    body: BodyController
    """
    def __init__(self, ip: str | None = None) -> None:
        self.sr: SpeechRecognitionClient = SpeechRecognitionClient(ip=ip)
        self.tts: Text2SpeechClient = Text2SpeechClient(ip=ip)
        self.face: FaceRecognitionClient = FaceRecognitionClient(ip=ip)
        self.express: ExpressionController = ExpressionController(ip=ip)
        self.body: BodyController = BodyController(ip=ip)
        pass

    def close(self) -> None:
        self.sr.close()
        self.tts.close()
        self.face.close()
        self.express.close()
        self.body.close()
        pass

    # n回分間を差し込む
    def pause(self, n):
        for i in range(n):
            self.tts.speech(" ")

    def start(self) -> None:
        rbc = RobotBodyController()

        while True:
            define_motion(rbc, 'そうだよね，どうしようか迷うね')
            time.sleep(3)
            

        # res = "こんにちは。オウム返しをします。"  # エリカに発話させる内容
        # print(res)

        # self.tts.speech(res)
        # self.express.express(ExpressionType.FullSmile)  # エリカの表情
        # self.body.play_motion(MotionType.Greeting)  # エリカの動作

        while True:
            pass


if __name__ == "__main__":
    model = SampleModel()
    model.start()

