from dslclib import (
    SpeechRecognitionClient,
    Text2SpeechClient,
    # FaceRecognitionClient,
    ExpressionController,
    BodyController,
    ExpressionType,
    MotionType,
    STTRecognitionType,
)
import random
import time
import asyncio
from functools import partial
import threading


# GPT4で生成生成する関数を取得
from chat_tohoku_v1 import main, get_args, start_conversation, shizuka_response

# 使うモジュールを取得
from utils import (
    extract_emotion_and_motion, take_time, is_period, is_exclamation, is_hatena, kanji_to_kana, is_safty_end, define_motion, is_santen, sentence_length_and_time, is_comma
)
# 使うモジュールを取得
from module import RobotBodyController, RobotExpressionController, CorrespondUserExpression, RobotSpeechController


SYSTEM_BYE_UTT = 'あ、ごめん、そろそろ時間だから帰らなきゃ。続きはまた話そう！ばいばい！'
SYSTEM_RESET_UTT = 'システムをリセットしました。'
SYSTEM_END_UTT = '対話の時間が終了しました。評価をお願いします。'
MAX_NUM_QUEUE = 10000  # ここを大きくしたら解決？

class SampleModel():
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
        # self.face: FaceRecognitionClient = FaceRecognitionClient(ip=ip)
        self.express: ExpressionController = ExpressionController(ip=ip)
        self.body: BodyController = BodyController(ip=ip)
        pass

    def close(self) -> None:
        self.sr.close()
        self.tts.close()
        # self.face.close()
        self.express.close()
        self.body.close()
        pass

    
    # 音声認識のタイムアウトを操る関数
    def get_speech_recognition_output(self):
        while event.wait():
            self.output = self.sr.listen()
            event.clear()

    # n回分間を差し込む
    def pause(self, n):
        for _ in range(n):
            self.tts.speech(" ", wait_queue=True, max_num_queue=MAX_NUM_QUEUE)

    # 対話終了直前のセリフ
    def end_speech(self):
        print(f"システム : {SYSTEM_BYE_UTT}")
        # ここに動きを入れたい
        self.tts.speech("あ、ごめん", speed=130, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
        self.pause(1)
        self.tts.speech("そろそろ時間だから帰らなきゃ", speed=130, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
        self.pause(2)
        self.tts.speech("続きはまた話そう！", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
        self.pause(3)
        self.tts.speech("バイバイ！", speed=100, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)

        # 動作の定義
        time.sleep(2)
        self.body.play_motion("greeting")
        time.sleep(4) # 3だとはやい
        self.body.play_motion("right_hand_byebye")
        time.sleep(3)
        self.body.play_motion(MotionType.RightHandBasePosition)

    # def threading_motion(self, sentence="", gptemotion="", gptmotion=""):
    #     time.sleep(sentence_length_and_time(sentence))
    #     # ここで robotbodycontoller を渡せば解決する？
    #     define_motion(robotbodycontoller, sentence, gptemotion, gptmotion)

    def start(self) -> None:
        args = get_args()
        robotbodycontroller = RobotBodyController()
        robotexpressioncontroller = RobotExpressionController()
        corresponduserexpression = CorrespondUserExpression()
        robotspeechcontroller = RobotSpeechController()
        
        # 対話の準備
        start_main_convesation_time = float('inf') # スタート時間（とりあえず最大値を代入，システムリセットでスタート）
        main_client, slot_clients = start_conversation(args)
        is_first_end = True # ５分の対話が最初に終わったときを判定
        is_system_reset = False # システムリセットが行われたかどうかを判定
        first_conversation_flag = True # 最初の一往復は固定する
        uttr = ""
        uttr_merge = ""
        pre_express = ""

        # タイムアウト用のthreadの起動
        global event
        start_shizuka_res = 0.0
        event = threading.Event()
        input_thread = threading.Thread(target=self.get_speech_recognition_output)
        input_thread.start()

        # 対話開始
        while True:
            try:
                # カスタムタイムアウトオン
                if args.is_time_out and first_conversation_flag == False:
                # threadでタイムアウトをなくす
                    uttr_merge = ""
                    while True:
                        is_speaking = False
                        event.set()
                        
                        speech_lasting_time = time.time()
                        while time.time() - speech_lasting_time < 1.6:
                            if not event.is_set():
                                is_speaking =True
                                break

                        event.clear()
                        if not is_speaking and uttr_merge != "":
                            break
                        if time.time() - start_shizuka_res < 4:
                            self.output = ""
                            continue

                        if self.output:
                            cond = self.output.type  # ユーザが発話常態かどうか
                            uttr = self.output.result  # ユーザの発話
                            if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                                if random.random() < 0.3:
                                    self.body.play_motion(MotionType.Nod)  # うなずく
                            else:
                                uttr_merge += uttr
                    
                    self.output = ""
                    print(f'ユウキ : {uttr_merge}')
                
                # 最初の一往復の会話
                elif first_conversation_flag and is_system_reset:
                    output = self.sr.listen(interim=False)  # 聞き取ったユーザの発話について，interim=Falseのほうがストックされるので良さそう
                    cond = output.type  # ユーザが発話状態かどうか
                    uttr = output.result  # ユーザの発話
                    if len(uttr) <=5:
                        continue
                    elif len(uttr) > 5 and uttr != 'そろそろ準備しないとね':   # 「そろそろ準備しないとね」という発話でない場合
                        print(f"システム : そろそろ準備しないとね。から対話を開始してください。")
                        self.tts.speech("そろそろ準備しないとね。から対話を開始してください。", wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                        continue
                    else:
                        main_client.add_user_input(uttr) # 対話履歴に追加
                        print(f"ユウキ : {uttr}")
                    
                    # if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                    #     continue

                # 「システムリセット」するとき
                else:
                    output = self.sr.listen(interim=False)  # 聞き取ったユーザの発話について，interim=Falseのほうがストックされるので良さそう
                    cond = output.type  # ユーザが発話常態かどうか
                    uttr = output.result
                    print(f"ユウキ : {uttr}")
                    
                    # if cond == STTRecognitionType.InterimResult:  # 発話途中ならば
                    #     continue
                    
                # システムリセットの実装
                if "システムリセット" in uttr or "システムリセット" in uttr_merge:
                    # 諸々の初期化
                    start_main_convesation_time = time.time()
                    main_client, slot_clients = start_conversation(args)
                    is_system_reset = True # システムリセットが行われたかどうかを判定
                    is_first_end = True # ５分の対話が最初に終わったときを判定
                    first_conversation_flag = True # 最初の一往復は固定する
                    uttr_merge = ""

                    # 評価開始
                    print(f"システム : {SYSTEM_RESET_UTT}")
                    self.tts.speech(SYSTEM_RESET_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                    continue
                
                elif is_system_reset == False:
                    print("システム : システムをリセットしてください")
                    self.tts.speech("システムをリセットしてください", wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                    continue

                # システムリセット後の最初の一往復は固定
                elif (uttr == 'そろそろ準備しないとね' or uttr_merge == 'そろそろ準備しないとね') and is_system_reset:
                    if first_conversation_flag:
                        start_shizuka_res = time.time()
                        # 最初のシズカの応答
                        self.pause(2) # ここだけ生成時間が無いので間をとる
                        print("シズカ : そうだね、ユウキ。")
                        self.tts.speech("そうだね、ユウキ。", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                        robotbodycontroller('nod_deep')
                        self.pause(2)

                        print("シズカ : まずは会場から決めようか。")
                        self.tts.speech("まずは会場から決めようか。", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                        self.pause(2)

                        print("シズカ : 学内にする？")
                        self.tts.speech("学内にする？", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                        self.pause(1)

                        self.tts.speech("それとも", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)

                        print("シズカ : それとも学外のレストランとかにする？")
                        self.tts.speech("学外のレストランとかにする？", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                        
                        # GPT4の履歴に残す
                        sentence = "*平常* *うなずく* そうだね、ユウキ。 *平常* まずは会場から決めようか。 *期待* 学内にする？ *期待* それとも学外のレストランにする？"
                        main_client.add_assistant_response(sentence)

                        # 次回以降はGPT4の生成
                        first_conversation_flag = False

                        time.sleep(2)
                        pres = ["そうだね、ユウキ。", "まずは会場から決めようか。"]
                        for pre in pres:
                            time.sleep(sentence_length_and_time(pre))
                        robotbodycontroller('rhp')
                        time.sleep(2)
                        robotbodycontroller('rbp')
                        robotbodycontroller('lhp')
                        time.sleep(2)
                        robotbodycontroller('lbp')
                
                # 対話時間終了後
                elif time.time() - start_main_convesation_time > args.max_time:
                    # 最初に終わったときだけ一言加える
                    if is_first_end:
                        self.end_speech()
                        is_first_end = False
                        self.pause(4)
                    
                    robotbodycontroller("greeting")
                    self.body.play_motion(MotionType.Greeting)  # エリカの動作

                    print(f"システム : {SYSTEM_END_UTT}")
                    self.tts.speech(SYSTEM_END_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)

                # 対話中
                else:
                    start_shizuka_res = time.time()
                    for sentence in shizuka_response(args, main_client, slot_clients, uttr):  # GPT4で1行ずつ発話生成
                        if sentence != '。':
                            pass
                        # 間を決めて，シズカの発話の後に挿入する
                        if is_hatena(sentence) or is_exclamation(sentence) or is_period(sentence):
                            time_stop = 1 # 間の間隔（秒単位ではない）

                        # 三点リーダーのときは長めに間をとる
                        elif is_santen(sentence):
                            time_stop = 3

                            # ここに悩む動作を入れても良さそう
                            # スピードを下げる
                            # ピッチ低め

                        else:
                            time_stop = 0
                        
                        # ここで抽出した感情や動作によってシズカの挙動を決める
                        # express, speech_param, motion, main_sentence = extract_emotion_and_motion(sentence)  # 文中の感情を抽出
                        express, motion, main_sentence = extract_emotion_and_motion(sentence)  # 文中の感情を抽出
                        
                        # 感情が切り替わるタイミングではさらに間を差し込む
                        if express == "平常" and pre_express == "":
                            pass
                        elif express == "" and pre_express == "平常":
                            pass
                        elif express != pre_express:
                            self.pause(2)
                        
                        # max_tokenの上限で打ち切られた途中の文は捨てて次の発話へ
                        if is_safty_end(main_sentence) == False:
                            continue
                        
                        # ルールベースエラー訂正
                        main_sentence_error_translation = kanji_to_kana(main_sentence)
                        print(f"シズカ : {main_sentence_error_translation}")

                        # デバッグモードのときは色々出力
                        if args.debug:
                            GRAY = "\033[90m"
                            RESET = "\033[0m"
                            try:
                                if pre_express:
                                    print(f"{GRAY}[DEBUG] express={pre_express}, motion={motion}, time_stop={time_stop}s{RESET}")
                                else:
                                    print(f"{GRAY}[DEBUG] express={express}, motion={motion}, time_stop={time_stop}s{RESET}")
                            except:
                                print(f"{GRAY}[DEBUG] express={express}, motion={motion}, time_stop={time_stop}s{RESET}")
                            
                        # ！のときはボリュームを上げる
                        if is_exclamation(main_sentence_error_translation):
                            add_volume = 50
                            add_speed = 0
                            add_pitch = 0
                        # …のときは，ボリュームを下げる，スピードゆっくり，ピッチ下げる
                        elif is_santen(main_sentence_error_translation):
                            add_volume = -50
                            add_speed = -30
                            add_pitch = -10

                        else:
                            add_volume = 0
                            add_speed = 0
                            add_pitch = 0

                        # 発話 & 表情 (感情が出力された場合どちらも必ず値があるので、expressのみのif分岐でまとめる)
                        if pre_express and not express:
                            express = pre_express
                        
                        if express:
                            robotspeechcontroller.robotSpeech(
                                main_sentence_error_translation, express, add_volume, add_speed, add_pitch
                            )
                            robotexpressioncontroller(express)
                        else:
                            self.tts.speech(main_sentence_error_translation, speed=110, volume=100+add_volume, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                            self.express.express(ExpressionType.Smile)
                            
    
                        # 間を挿入
                        self.pause(time_stop)

                        # 文の長さに応じてsleepしてから動作
                        time.sleep(sentence_length_and_time(main_sentence_error_translation))
                        define_motion_thread = threading.Thread(target=define_motion, args=(robotbodycontroller, main_sentence_error_translation, motion, express))
                        define_motion_thread.start()
                        
                        # 発話パラメータ, 表情, 動作の保持
                        if is_exclamation(main_sentence_error_translation) or is_hatena(main_sentence_error_translation) or is_period(main_sentence_error_translation):
                            # todo: is_santen も追加?
                            pre_express = ""

                        else:
                            pre_express = express

                        # 句点「。」まで表情を保つ
                        if is_period(main_sentence_error_translation):
                            pass

                        # デバッグモードのときは現在時間を表示
                        if args.debug:
                            GRAY = "\033[90m"
                            RESET = "\033[0m"
                            print(f"{GRAY}time: {time.time() - start_main_convesation_time}s{RESET}")
                        # 評価終了判定 (5分経過)
                        if time.time() - start_main_convesation_time > args.max_time:
                            time.sleep(sentence_length_and_time(main_sentence_error_translation))
                            self.end_speech()
                            self.pause(4)
                            robotbodycontroller("greeting")
                            print(f"システム : {SYSTEM_END_UTT}")
                            self.tts.speech(SYSTEM_END_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                            is_first_end = False
                            break

                        
                        
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

