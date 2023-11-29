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
import random

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

    def taiwa(self, pitch, speed=120):
        # self.tts.speech(f"ピッチ：{pitch}")
        # self.pause(2)
        self.tts.speech("うん、", speed=speed, pitch=pitch)
        self.tts.speech("そうだね。", speed=speed, pitch=pitch)
        self.pause(2)
        self.tts.speech("まずは会場から決めようか。", speed=speed, pitch=pitch)
        self.pause(2)
        self.tts.speech("学内でやるか、", speed=speed, pitch=pitch)
        self.tts.speech("それとも学外のレストランとかにする？", speed=speed, pitch=pitch)
        self.pause(4)

    def start(self) -> None:
        l = range(100,126,5)
        for i, p in enumerate(random.sample(l, len(l))):
            print(i, p)
            self.tts.speech(f"{i}")
            self.pause(2)
            self.taiwa(p)
        # self.taiwa(100)
        # self.taiwa(105)
        # self.taiwa(110)
        # self.taiwa(115)
        # self.taiwa(120)
        # self.taiwa(125)
        # self.taiwa(130)
        # self.taiwa(135)
        # self.taiwa(140)
    


        self.express.express(ExpressionType.FullSmile)  # エリカの表情
        self.body.play_motion(MotionType.Greeting)  # エリカの動作

        while True:
            try:
                output = self.sr.listen(interim=True)  # 聞き取ったユーザの発話について
                cond = output.type  # ユーザが発話常態かどうか
                uttr = output.result  # ユーザの発話

                if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                    if random.random() > 0.3:
                        self.body.play_motion(MotionType.Nod)  # うなずく
                    else:
                        self.body.play_motion(MotionType.NodDeep)  # 深くうなずく
                    continue
                
                print(uttr)
                if uttr in ("さようなら", "さよなら"):
                    self.tts.speech("ありがとうございました。さようなら。")
                    break

                # オウム返しをさせる
                # self.tts.speech(f"はい、{uttr}、ですね" , speed=150, volume=200, pitch=150)
                

            except KeyboardInterrupt:
                print("対話を終了します。")
                break
            except Exception as e:
                print(f"予期せぬエラー`{e}`です。")
                raise e

        print("対話が正常に終了しました。")
        self.close()


if __name__ == "__main__":
    model = SampleModel()
    model.start()

