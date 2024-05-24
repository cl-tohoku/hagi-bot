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
    Sample dialogue model for parroting

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
        res = "こんにちは。オウム返しをします。"  # "hello, I'm parroting."
        print(res)

        self.tts.speech(res)
        self.express.express(ExpressionType.FullSmile)  # Erica's facial expression
        self.body.play_motion(MotionType.Greeting)  # Erica's motion

        while True:
            try:
                output = self.sr.listen(interim=True)  # On the user's speech that was heard
                cond = output.type  # Whether the user is in a speech state or not.
                print(cond)
                uttr = output.result  # user utterance

                if cond == STTRecognitionType.InterimResult:  # If in the middle of speech.
                    if random.random() > 0.3:
                        self.body.play_motion(MotionType.Nod)  # nodding
                    else:
                        self.body.play_motion(MotionType.NodDeep)  # nodding deeply
                    continue
                
                print(uttr)
                if uttr in ("さようなら", "さよなら"): # If the user says goodbye
                    self.tts.speech("ありがとうございました。さようなら。") # "Thank you. Goodbye."
                    break

                # オウム返しをさせる
                self.tts.speech(f"はい、{uttr}、ですね" , speed=150, volume=200, pitch=150) # "Yes, it is {uttr}."
                
            except KeyboardInterrupt:
                print("対話を終了します。") # "End of dialogue."
                break
            except Exception as e:
                print(f"予期せぬエラー`{e}`です。") # "Unexpected error."
                raise e

        print("対話が正常に終了しました。") # "The dialogue has ended successfully."
        self.close()


if __name__ == "__main__":
    model = SampleModel()
    model.start()

