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
import asyncio
from functools import partial
import threading

# GPT4で生成生成する関数を取得
from .src.gpt_response import get_args, start_conversation, shizuka_response

# 使うモジュールを取得
from .src.utils import (
    extract_emotion_and_motion, take_time, is_period, is_exclamation, is_hatena, kanji_to_kana, is_safty_end, define_motion, is_santen, sentence_length_and_time, is_comma
)
# 使うモジュールを取得
from .src.avatar import RobotBodyController, RobotExpressionController, CorrespondUserExpression, RobotSpeechController


SYSTEM_BYE_UTT = 'あ、ごめん、そろそろ時間だから帰らなきゃ。続きはまた話そう！ばいばい！'  # "Sorry, it's time to go back. Let's talk again later. Bye-bye!"
SYSTEM_RESET_UTT = 'システムをリセットしました。'  # "The system has been reset."
SYSTEM_END_UTT = '対話の時間が終了しました。評価をお願いします。'  # "The conversation time has ended. Please evaluate the dialogue."
MAX_NUM_QUEUE = 10000

class SampleModel():
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
    output = ""

    def __init__(self, ip: str | None = None) -> None:
        self.sr: SpeechRecognitionClient = SpeechRecognitionClient(ip=ip)
        self.tts: Text2SpeechClient = Text2SpeechClient(ip=ip)
        self.express: ExpressionController = ExpressionController(ip=ip)
        self.body: BodyController = BodyController(ip=ip)
        pass

    def close(self) -> None:
        self.sr.close()
        self.tts.close()
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
        print(f"システム : {SYSTEM_BYE_UTT}") # "System: {SYSTEM_BYE_UTT}"
        self.tts.speech("あ、ごめん", speed=130, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE) # "Sorry,"
        self.pause(1)
        self.tts.speech("そろそろ時間だから帰らなきゃ", speed=130, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE) # "it's time to go back."
        self.pause(2)
        self.tts.speech("続きはまた話そう！", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE) # "Let's talk again later!"
        self.pause(3)
        self.tts.speech("バイバイ！", speed=100, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)  # "Bye-bye!"

        # Motion Definition
        time.sleep(2)
        self.body.play_motion("greeting")
        time.sleep(4) # 3 is a little too fast
        self.body.play_motion("right_hand_byebye")
        time.sleep(3)
        self.body.play_motion(MotionType.RightHandBasePosition)

    def start(self) -> None:
        args = get_args()
        robotbodycontroller = RobotBodyController()
        robotexpressioncontroller = RobotExpressionController()
        corresponduserexpression = CorrespondUserExpression()
        robotspeechcontroller = RobotSpeechController()
        
        # 対話の準備
        start_main_convesation_time = float('inf') # Start time (assign maximum value for now, start with system reset)
        main_client, slot_clients = start_conversation(args)
        is_first_end = True # Determine when the first five-minute dialogue ends.
        is_system_reset = False # Determines whether a system reset has taken place
        first_conversation_flag = True # Fix the first round.
        uttr = ""
        uttr_merge = ""
        pre_express = ""

        # Launching threads for timeouts.
        global event
        start_shizuka_res = 0.0
        event = threading.Event()
        input_thread = threading.Thread(target=self.get_speech_recognition_output)
        input_thread.start()

        # Conversation start
        while True:
            try:
                # Customized timeout for speech recognition
                if args.is_time_out and first_conversation_flag == False:
                # Eliminate timeouts with threads
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
                            cond = self.output.type  # Whether the user is in a speech state or not
                            uttr = self.output.result  # user utterance
                            if cond == STTRecognitionType.InterimResult:  # if in the middle of speech
                                if random.random() < 0.3:
                                    self.body.play_motion(MotionType.Nod)  # nodding
                            else:
                                uttr_merge += uttr
                    
                    self.output = ""
                    print(f'ユウキ : {uttr_merge}')  # "Yuki: {uttr_merge}"
                
                # The first round conversation
                elif first_conversation_flag and is_system_reset:
                    output = self.sr.listen(interim=False)
                    cond = output.type  # Whether the user is in a speech state or not
                    uttr = output.result  # user utterance
                    if len(uttr) <=5:
                        continue
                    elif len(uttr) > 5 and uttr != 'そろそろ準備しないとね':   # if the user's utterance is NOT "it's time to get ready"
                        print(f"システム : そろそろ準備しないとね。から対話を開始してください。") # "System: You need to get ready soon. Please start the conversation."
                        self.tts.speech("そろそろ準備しないとね。から対話を開始してください。", wait_queue=True, max_num_queue=MAX_NUM_QUEUE)   # "You need to get ready soon. Please start the conversation."
                        continue
                    else:
                        main_client.add_user_input(uttr) # Add to dialogue history
                        print(f"ユウキ : {uttr}")  # "Yuki: {uttr}"

                # 「システムリセット」するとき
                else:
                    output = self.sr.listen(interim=False)
                    cond = output.type  # Whether the user is in a speech state or not
                    uttr = output.result
                    print(f"ユウキ : {uttr}") # "Yuki: {uttr}"
                    
                # Implementation of system reset.
                if "システムリセット" in uttr or "システムリセット" in uttr_merge:  # If "system reset" is in the user's utterance
                    # initialization
                    start_main_convesation_time = time.time()
                    main_client, slot_clients = start_conversation(args)
                    is_system_reset = True # Determines whether a system reset has taken place
                    is_first_end = True # Determine when the first five-minute dialogue ends.
                    first_conversation_flag = True # Fix the first round.
                    uttr_merge = ""

                    # Evaluation start
                    print(f"システム : {SYSTEM_RESET_UTT}")  # "System: {SYSTEM_RESET_UTT}"
                    self.tts.speech(SYSTEM_RESET_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                    continue
                
                elif is_system_reset == False:
                    print("システム : システムをリセットしてください")  # "System: Please reset the system."
                    self.tts.speech("システムをリセットしてください", wait_queue=True, max_num_queue=MAX_NUM_QUEUE)  # "Please reset the system."
                    continue

                # First round after system reset fixed
                elif (uttr == 'そろそろ準備しないとね' or uttr_merge == 'そろそろ準備しないとね') and is_system_reset: # If the user's utterance is "it's time to get ready"
                    if first_conversation_flag:
                        start_shizuka_res = time.time()
                        # First Shizuka's response
                        self.pause(2)
                        print("シズカ : そうだね、ユウキ。")  # "Shizuka: That's right, Yuki."
                        self.tts.speech("そうだね、ユウキ。", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)  # "That's right Yuki."
                        robotbodycontroller('nod_deep')
                        self.pause(2)

                        print("シズカ : まずは会場から決めようか。")    # "Shizuka: Shall we decide on the venue first?"
                        self.tts.speech("まずは会場から決めようか。", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)  # "Shall we decide on the venue first?"
                        self.pause(2)

                        print("シズカ : 学内にする？") # "Shizuka: Shall we have it on campus?"
                        self.tts.speech("学内にする？", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)  # "Shall we have it on campus?"
                        self.pause(1)

                        self.tts.speech("それとも", speed=120, pitch=115, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)     # "Or"

                        print("シズカ : それとも学外のレストランとかにする？")    # "Shizuka: Or should we go to a restaurant outside of school?"
                        self.tts.speech("学外のレストランとかにする？", speed=120, pitch=117, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)     # "Should we go to a restaurant outside of school?"
                        
                        # Leave in GPT4 history
                        sentence = "*平常* *うなずく* そうだね、ユウキ。 *平常* まずは会場から決めようか。 *期待* 学内にする？ *期待* それとも学外のレストランにする？"  # "*neutral* *nod* That's right, Yuki. *nod* Shall we decide on the venue first? *Hope* Shall we have it on campus? *Hope* Or should we go to a restaurant outside of school?"
                        main_client.add_assistant_response(sentence)

                        # Generation of GPT4 in the next time
                        first_conversation_flag = False

                        time.sleep(2)
                        pres = ["そうだね、ユウキ。", "まずは会場から決めようか。"] # ["That's right, Yuki." "Shall we decide on the venue first?]"
                        for pre in pres:
                            time.sleep(sentence_length_and_time(pre))
                        robotbodycontroller('rhp')
                        time.sleep(2)
                        robotbodycontroller('rbp')
                        robotbodycontroller('lhp')
                        time.sleep(2)
                        robotbodycontroller('lbp')
                
                # After the conversation time
                elif time.time() - start_main_convesation_time > args.max_time:
                    # Only add words when first finish.
                    if is_first_end:
                        self.end_speech()
                        is_first_end = False
                        self.pause(4)
                    
                    robotbodycontroller("greeting")
                    self.body.play_motion(MotionType.Greeting)  # Erica's motion

                    print(f"システム : {SYSTEM_END_UTT}")   # "System: {SYSTEM_END_UTT}"
                    self.tts.speech(SYSTEM_END_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)

                # In the middle of the conversation
                else:
                    start_shizuka_res = time.time()
                    for sentence in shizuka_response(args, main_client, slot_clients, uttr):  # Speech generation one line at a time with GPT4.
                        if sentence != '。':
                            pass
                        # Pause and insert after Sizka's utterance.
                        if is_hatena(sentence) or is_exclamation(sentence) or is_period(sentence):
                            time_stop = 1 

                        # Longer pauses for "..."
                        elif is_santen(sentence):
                            time_stop = 3

                        else:
                            time_stop = 0
                        
                        # The emotions and behaviours extracted here determine Sizuka's behaviour.
                        express, motion, main_sentence = extract_emotion_and_motion(sentence)  # Extracting emotion from a sentence
                        
                        # Further pauses are inserted when emotions switch.
                        if express == "平常" and pre_express == "":  # If the emotion is "neutral" and the previous emotion is empty
                            pass
                        elif express == "" and pre_express == "平常": # If the emotion is empty and the previous emotion is "neutral"
                            pass
                        elif express != pre_express:
                            self.pause(2)
                        
                        # Sentences in the middle of a sentence that are terminated by the max_token limit are discarded and the next utterance is made.
                        if is_safty_end(main_sentence) == False:
                            continue
                        
                        # rule-based error correction
                        main_sentence_error_translation = kanji_to_kana(main_sentence)
                        print(f"シズカ : {main_sentence_error_translation}")

                        # Various outputs when in debug mode.
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
                            
                        # Turn up the volume when "!".
                        if is_exclamation(main_sentence_error_translation):
                            add_volume = 50
                            add_speed = 0
                            add_pitch = 0
                        # When "...", turn down the volume, slow down the speed and lower the pitch.
                        elif is_santen(main_sentence_error_translation):
                            add_volume = -50
                            add_speed = -30
                            add_pitch = -10

                        else:
                            add_volume = 0
                            add_speed = 0
                            add_pitch = 0

                        # Speech & Expression (both always have a value if emotion is output, so summarise with an if branch for express only).
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
                            
    
                        
                        self.pause(time_stop)

                        # sleep depending on the length of the sentence, then operate.
                        time.sleep(sentence_length_and_time(main_sentence_error_translation))
                        define_motion_thread = threading.Thread(target=define_motion, args=(robotbodycontroller, main_sentence_error_translation, motion, express))
                        define_motion_thread.start()
                        
                        #  Speech parameters, facial expressions, retention of actions
                        if is_exclamation(main_sentence_error_translation) or is_hatena(main_sentence_error_translation) or is_period(main_sentence_error_translation):

                            pre_express = ""

                        else:
                            pre_express = express

                        #  Maintain facial expression until "."
                        if is_period(main_sentence_error_translation):
                            pass

                        # When in debug mode, the current time is displayed.
                        if args.debug:
                            GRAY = "\033[90m"
                            RESET = "\033[0m"
                            print(f"{GRAY}time: {time.time() - start_main_convesation_time}s{RESET}")
                        # Decision to end evaluation (5 min)
                        if time.time() - start_main_convesation_time > args.max_time:
                            time.sleep(sentence_length_and_time(main_sentence_error_translation))
                            self.end_speech()
                            self.pause(4)
                            robotbodycontroller("greeting")
                            print(f"システム : {SYSTEM_END_UTT}")   # "System: {SYSTEM_END_UTT}"
                            self.tts.speech(SYSTEM_END_UTT, wait_queue=True, max_num_queue=MAX_NUM_QUEUE)
                            is_first_end = False
                            break

                        
                        
            except KeyboardInterrupt:
                print("対話を終了します。")     # "End of dialogue."
                break
            except Exception as e:
                print(f"予期せぬエラー`{e}`です。")     # "Unexpected error."
                raise e

        print("対話が正常に終了しました。")     # "The dialogue has ended successfully."
        self.close()


if __name__ == "__main__":
    model = SampleModel()
    model.start()

