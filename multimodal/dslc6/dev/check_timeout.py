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
import threading
import time

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
    output = ""

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

    def get_speech_recognition_output(self):
        while event.wait():
            print(1)
            self.output = self.sr.listen()
            event.clear()

    def start(self) -> None:
        # res = "こんにちは。オウム返しをします。"  # エリカに発話させる内容
        # print(res)
        # self.tts.speech(res)  # エリカに発話させる
        # self.express.express(ExpressionType.FullSmile)  # エリカの表情
        # self.body.play_motion(MotionType.Greeting)  # エリカの動作

        # self.tts.speech("昨日youtuberのアカウントがBANされたんだって")
        # self.tts.speech("金色")
        self.tts.speech("プレゼントの包装紙の色は金でいい？")
        self.tts.speech("")
        self.tts.speech("金色")
        
        


        global event
        event = threading.Event()
        input_thread = threading.Thread(target=self.get_speech_recognition_output)
        input_thread.start()

        while True:
            try:
                # if args.is_time_out == False:
                uttr_merge = ""
                
                while True:
                    print(0)
                    is_speaking = False
                    event.set()
                    start_time = time.time()
                    while time.time() - start_time < 2:
                        if not event.is_set():
                            print(2)
                            is_speaking =True
                            break

                    event.clear()
                    print(3)
                    if not is_speaking and uttr_merge != "":
                        print("Timeout")
                        break
                        # print(uttr_merge)

                    if self.output:
                        print(4)
                        cond = self.output.type  # ユーザが発話常態かどうか
                        uttr = self.output.result  # ユーザの発話
                        # print("uttr:" + uttr) # debug
                        if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                            if random.random() > 0.3:
                                self.body.play_motion(MotionType.Nod)  # うなずく
                            else:
                                self.body.play_motion(MotionType.NodDeep)  # 深くうなずく
                        else:
                            uttr_merge += uttr
                    
                self.output = ""
                    
                    # print(uttr)
                if uttr_merge in ("さようなら", "さよなら"):
                    self.tts.speech("ありがとうございました。さようなら。")
                    break

                # オウム返しをさせる
                print(uttr_merge)
                self.tts.speech(f"はい、{uttr_merge}、ですね" , speed=150, volume=200, pitch=150)

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