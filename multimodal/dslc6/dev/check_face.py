from dslclib import (
    SpeechRecognitionClient,
    Text2SpeechClient,
    FaceRecognitionClient,
    ExpressionController,
    BodyController,
    ExpressionType,
    MotionType,
    STTRecognitionType,
    EmotionType,
)
import random
import time
import json

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
        res = "こんにちは。オウム返しをします。"  # エリカに発話させる内容
        print(res)

        self.tts.speech(res)
        self.express.express(ExpressionType.FullSmile)  # エリカの表情
        self.body.play_motion(MotionType.Greeting)  # エリカの動作
        
        # その瞬間の感情
        # decoder = json.JSONDecoder()
        # face_json = decoder.raw_decode(self.face.receive_line())
        # print(face_json)
        
        # 10回計測した集計値（多数決)
        face_output = self.face.listen(self.face.summarize_times)
        print(face_output)

        while True:
            face_output = self.face.listen(self.face.summarize_times)
            print(face_output.emotion, face_output.emotion_score)
            # if (
            #     face_output.emotion 
            #     in
            #     [EmotionType.Anger, 
            #     EmotionType.Disgust,
            #     EmotionType.Fear,
            #     EmotionType.Happiness,
            #     EmotionType.Neutral,
            #     EmotionType.Sadness, 
            #     EmotionType.Surprise,]
            #     ):
            #     print(face_output.emotion)
            
            # face_json = decoder.raw_decode(self.face.receive_line())
            # print(face_json)
            # print(face_json["emotion_class"], face_json["emotion_score"])


        while True:
            try:
                output = self.sr.listen(interim=True)  # 聞き取ったユーザの発話について
                cond = output.type  # ユーザが発話常態かどうか
                print(cond)
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
                self.tts.speech(f"はい、{uttr}、ですね" , speed=150, volume=200, pitch=150)
                
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

