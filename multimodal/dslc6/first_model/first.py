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

# GPT4で生成生成する関数を取得
import sys
from avatarchat_tohoku_v1 import get_shizuka_response

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

    def start(self) -> None:
        res = "こんにちは。GPT4で発話するファーストモデルです。"  # エリカに発話させる内容
        print(res)

        self.tts.speech(res)  # エリカに発話させる
        # self.tts.speech("ビビンバマジでからかったな")
        self.tts.speech("それはいいですね。", speed=110, volume=200, pitch=120)
        self.tts.speech("それは残念ですね。", speed=100, volume=100, pitch=90)
        self.tts.speech("楽しみですね。", speed=100, volume=150, pitch=110)
        self.tts.speech("そんなことがあったんですか！", speed=120, volume=250, pitch=100)
        self.tts.speech("それは良くないと思います。", speed=100, volume=230, pitch=85)
        self.tts.speech("それは恐ろしいことですね。", speed=120, volume=250, pitch=100)
        self.tts.speech("いや、何を言っているのかわかりません。", speed=100, volume=100, pitch=80)
        self.tts.speech("あなたのことを信じています。", speed=100, volume=100, pitch=110)
        self.tts.speech("机の上に本があります。", speed=100, volume=100, pitch=100)
        self.tts.speech("それはいいですね。", speed=120, volume=200, pitch=120)
        # self.tts.speech("200だと早口すぎるな", volume=400)
        # self.tts.speech("volume200だとどうかな")
        self.express.express(ExpressionType.FullSmile)  # エリカの表情
        self.body.play_motion(MotionType.Greeting)  # エリカの動作

        
        while True:
            try:
                output = self.sr.listen(interim=False)  # 聞き取ったユーザの発話について
                cond = output.type  # ユーザが発話常態かどうか
                uttr = output.result  # ユーザの発話

                # ユーザの発話の誤り訂正


                # ユーザの発話状態によって変更する部分（フィラー、表情のミラーリング）

                if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                    if random.random() > 0.3:
                        self.body.play_motion(MotionType.Nod)  # うなずく
                    else:
                        self.body.play_motion(MotionType.NodDeep)  # 深くうなずく
                    continue
                
                print(uttr)  # ユーザの発話の出力

                # 対話の終了
                if uttr in ("さようなら", "さよなら"):
                    self.tts.speech("ありがとうございました。さようなら。")
                    break


                # オウム返しをさせる
                # self.tts.speech(f"はい、{uttr}、ですね", speed=100, volume=100, pitch=110)
                
                # GPT４に発話生成させる
                shizuka_res = get_shizuka_response(uttr)
                self.tts.speech(shizuka_res)


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

