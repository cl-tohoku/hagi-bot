from dslclib import (
    SpeechRecognitionClient,
    Text2SpeechClient,
    ExpressionController,
    BodyController,
    ExpressionType,
    MotionType,
    STTRecognitionType,
)
import random
import time

class RobotBodyController(object):
    def __init__(self, ip: str | None = None) -> None:
        self.body: BodyController = BodyController(ip=ip)
        pass

    def __call__(self, key):
        # ここにmotionを追加していく
        if key == "greeting":
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
        elif key == "lhy":
            self.body.play_motion("left_hand_you")
        # elif key == "":
        #     self.body.play_motion()
        elif key == "setgazerand":
            r_x = random.uniform(-0.04, 0.04)
            r_y = random.uniform(-0.04, 0.04)
            self.setGaze("eye", 0.0 + r_x, 1.2 + r_y, 1.5)
        elif key == "setgazedown":
            self.body.play_motion("greeting_deep_head")
            self.body.play_motion("greeting_deep_eye")
        elif key == "positivemove":
            start_time = time.time()
            rcommands = [
                'right_hand_beatstroke_palmup',
                'left_hand_beatstroke_palmup',
                'right_hand_beatstroke_palmside',
                'left_hand_beatstroke_palmside',
            ]
            while time.time() - start_time < 1:
                for command in rcommands:
                    self.body.play_motion(command)

    def playMotion(self, motion):
        self.body.play_motion(motion)

    def setGaze(self, type=["eye", "head"], x=0, y=0, z=0):
        # 正面方向:z軸，右方向:x軸，上方向:y軸
        # (例)
        #   正面に向く: (0.0, 1.2, 1.5)
        #   右に向く:   (1.0, 1.2, 1.5)
        #   左に向く:   (-1.0, 1.2, 1.5)
        if type == ["eye", "head"]:
            self.body.gaze(direction=(x, y, z))
        elif "eye" in type:
            self.body.gaze(eye=(x, y, z))
        else:
            self.body.gaze(head=(x, y, z))

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
    def __init__(self, module, ip: str | None = None) -> None:
        self.sr: SpeechRecognitionClient = SpeechRecognitionClient(ip=ip)
        self.tts: Text2SpeechClient = Text2SpeechClient(ip=ip)
        # self.face: FaceRecognitionClient = FaceRecognitionClient(ip=ip)
        self.express: ExpressionController = ExpressionController(ip=ip)
        self.body: BodyController = BodyController(ip=ip)
        self.robotbodycontroller = module
        pass

    def close(self) -> None:
        self.sr.close()
        self.tts.close()
        # self.face.close()
        self.express.close()
        self.body.close()
        pass

    def pause(self, n):
        for _ in range(n):
            self.tts.speech(" ")

    def start_speach(self):
        self.pause(2) # ここだけ生成時間が無いので間をとる
        print("シズカ : そうだね、ユウキ。")
        self.tts.speech("そうだね、ユウキ。", speed=120)
        self.robotbodycontroller('nod_deep')
        self.pause(2)

        print("シズカ : まずは会場から決めようか。")
        self.tts.speech("まずは会場から決めようか。", speed=120)
        self.pause(2)

        print("シズカ : 学内にする？")
        self.tts.speech("学内にする？", speed=120)
        self.pause(1)

        print("シズカ : それとも学外のレストランとかにする？")
        self.tts.speech("それとも学外のレストランとかにする？", speed=120)

        time.sleep(0.4)
        pres = ["そうだね、ユウキ。", "まずは会場から決めようか。"]
        for pre in pres:
            print(self.sentence_length_and_time(pre))
            time.sleep(self.sentence_length_and_time(pre))
        self.robotbodycontroller('rhp')
        time.sleep(2)
        self.robotbodycontroller('rbp')
        self.hatena_motion("それとも学外のレストランとかにする？")

    def is_period(self, sentence):
        if sentence.endswith("。"):
            return True
        else:
            return False

    # ！のときは True を返す．他のときは None を返す
    def is_exclamation(self,sentence):
        if sentence.endswith("！") or sentence.endswith("!"):
            return True
        else:
            return False

    # ？のときは True を返す．他のときは None を返す
    def is_hatena(self,sentence):
        if sentence.endswith("？") or sentence.endswith("?"):
            return True
        else:
            return False

    # 、のときは True を返す．他のときは None を返す
    def is_comma(self,sentence):
        if sentence.endswith("、"):
            return True
        else:
            return False

    # …のときは True を返す．他のときは None を返す
    def is_santen(self,sentence):
        if sentence.endswith("…"):
            return True
        else:
            return False

    def hatena_motion(self, sentence):
        if self.is_hatena(sentence):
            print("question")
            if len(sentence) > 13:
                time.sleep((len(sentence) - 13) * 0.2)
            self.robotbodycontroller('lhp')
            time.sleep(2)
            self.robotbodycontroller('lbp')
    
    def sentence_length_and_time(self, sentence):
        time_per_ten_letter = 1.6  # ここは計測してみて試す
        one_pause = 0.15

        if self.is_comma(sentence):
            add = one_pause
        elif self.is_hatena(sentence) or self.is_period(sentence) or self.is_exclamation(sentence):
            add = one_pause * 2
        elif self.is_santen(sentence):
            add = one_pause * 4
        else:
            add = 0

        return (len(sentence) / 10) * time_per_ten_letter + add

    def start(self) -> None:
        res = "こんにちは。オウム返しをします。"  # エリカに発話させる内容
        print(res)

        self.tts.speech(res)
        self.express.express(ExpressionType.FullSmile)  # エリカの表情
        self.body.play_motion(MotionType.Greeting)  # エリカの動作

        while True:
            try:
                output = self.sr.listen(interim=True)  # 聞き取ったユーザの発話について
                cond = output.type  # ユーザが発話常態かどうか
                # print(cond)
                uttr = output.result  # ユーザの発話

                if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                    self.robotbodycontroller("setgazerand")
                    if random.random() > 0.3:
                        self.body.play_motion(MotionType.Nod)  # うなずく
                    else:
                        self.body.play_motion(MotionType.NodDeep)  # 深くうなずく
                    continue
                
                print(uttr)
                if uttr in ("さようなら", "さよなら"):
                    self.tts.speech("ありがとうございました。さようなら。")
                    break
                
                # 秒数を測りたい
                # 5回の平均を測る
                # その後、この発話の間に挿入してみて試したい。
                print('2秒後に発話を開始します。')
                time.sleep(2)
                uttr_list = ["うーん、", "それも一つの手だね。", "でも、", "小林先生が顧問になってくれたことを祝う意味でも、", "ちょっと特別な雰囲気を出したいなって思ってるんだ。", "だから、", "学外のレストランでやるのはどうかな？"]
                uttr_motion_list =[]
                for _, uttr in enumerate(uttr_list):
                    if random.random() > 0.5:
                        self.tts.speech(uttr, speed=120)
                    else:
                        self.tts.speech(uttr, speed=125)
                    self.pause(2)
                
                for uttr in uttr_list:
                    print(uttr)
                    time.sleep(self.sentence_length_and_time(uttr))
                    self.hatena_motion(uttr)
                
            except KeyboardInterrupt:
                print("対話を終了します。")
                break
            except Exception as e:
                print(f"予期せぬエラー`{e}`です。")
                raise e

        print("対話が正常に終了しました。")
        self.close()


if __name__ == "__main__":
    module = RobotBodyController()
    # model = SampleModel(module)
    # model.start_speach()
    # module('rhp')
    # time.sleep(2)
    # module('rbp')

    print('2秒後に動き出します')
    time.sleep(2)
    module("悩む")