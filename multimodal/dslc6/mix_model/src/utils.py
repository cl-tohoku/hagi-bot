import re
import time
import tiktoken
import os
import pathlib
import csv
import datetime
import random

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

from avatar import RobotBodyController, RobotExpressionController, CorrespondUserExpression, RobotSpeechController

# 感情を取り出すモジュール
def extract_emotion_and_motion(sentence):
    '''
    1発話で感情*1+モーション*1まで
    デフォルトの発話速度を110に変えたので、元々110のものは115に、元々100のものは110に変更
    '''
    emotions = {
        '喜び', 
        '悲しみ', 
        '期待', 
        '驚き', 
        '怒り', 
        '恐れ', 
        '嫌悪', 
        '信頼', 
        '平常'  # 中立から平常に変更
        }
    motions = {
        'うなずく',
        '首を横に振る',
        '悩む',
        'お辞儀'
        }
    find_str = re.compile(r'\*(.+?)\*\s*')
    results = {'emotion': '', 'motion': ''}

    if founds := find_str.findall(sentence):
        main_sentence = find_str.sub('', sentence)
        for found in founds:
            if found in emotions and results['emotion'] == '':
                results['emotion'] = found
            elif found in motions and results['motion'] == '':
                results['motion'] = found

        if results['emotion']:
            express = results['emotion']
        else:
            express = ''

        if results['motion']:
            motion = results["motion"]
        else:
            motion = ''

        return express, motion, main_sentence
    
    else:
        express = ''
        motion = ''

        return express, motion, sentence

# 区切り文字によって間を変更するモジュール
def take_time(sentence):
    ma = 2 # 間の秒数
    if sentence.endswith("、"):
        return 0
    elif sentence.endswith("。"):
        time.sleep(ma)
        return ma
    elif sentence.endswith("？"):
        time.sleep(ma)
        return ma
    elif sentence.endswith("！"):
        time.sleep(ma)
        return ma

# 。のときは True を返す．他のときは None を返す
def is_period(sentence):
    if sentence.endswith("。"):
        return True
    else:
        return False

# ！のときは True を返す．他のときは None を返す
def is_exclamation(sentence):
    if sentence.endswith("！") or sentence.endswith("!"):
        return True
    else:
        return False

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

# 5つの区切り文字で正しく終了しているかどうか
def is_safty_end(sentence):
    if is_comma(sentence) or is_exclamation(sentence) or is_period(sentence) or is_hatena(sentence) or is_santen(sentence):
        return True
    else:
        return False

# 漢字をひらがなになおす
def kanji_to_kana(sentence):
    result = sentence
    # ほうと読む場合は大体’の’がつくので、’かた’と読む場合と区別する
    if 'の方' in sentence and '一方' not in sentence:
        result = sentence.replace('方', 'ほう')
    
    if '他' in sentence:
        result = sentence.replace('他', 'ほか')

    if '交通の便' in sentence:
        result = sentence.replace('交通の便', '交通のべん')
        
    if '僕' in sentence:
        result = sentence.replace('僕', '私')

    return result

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
            


# 文章に合わせてsleepする時間を計測する関数
def sentence_length_and_time(sentence):
    time_per_ten_letter = 1.6
    one_pause = 0.15
    if is_comma(sentence):
        add = one_pause
    elif is_hatena(sentence) or is_period(sentence) or is_exclamation(sentence):
        add = one_pause * 2
    elif is_santen(sentence):
        add = one_pause * 4
    else:
        add = 0
    sleep = (len(sentence) / 10) * time_per_ten_letter + add
    if sleep < 0.5:
        return (len(sentence) / 10) * time_per_ten_letter + add
    else:
        return (len(sentence) / 10) * time_per_ten_letter + add - 0.5

class ManageMoney:
    def __init__(self, prompt: str, output: str, file_path: str):
        self.tokenizer = tiktoken.get_encoding("cl100k_base")
        self.prompts: dict = prompt
        self.prompts_str: str
        self.output: str = output
        self.prompt_tokens: int = 0
        self.output_tokens: int = 0
        self.money: int = 0
        self.file_path: str = file_path

    def write_money_file(self):
        if not os.path.isfile(self.file_path):
            file = pathlib.Path(self.file_path)
            file.touch()
            with open(self.file_path, 'w') as fo:
                writer = csv.writer(fo)
                writer.writerow(['output_time', 'money', 'prompt_tokens', 'output_tokens', 'prompt', 'output'])
        
        with open(self.file_path, 'a') as fo:
            writer = csv.writer(fo)
            writer.writerow([datetime.datetime.now(), self.money, self.prompt_tokens, self.output_tokens, self.prompts_str, self.output])

    def prompts_to_str(self):
        self.prompts_str = ''.join([message['content'] for message in self.prompts])
            
    def count_token(self, sentence, mode):
        tokens = self.tokenizer.encode(sentence)
        if mode == 'prompt':
            self.prompt_tokens = len(tokens)
        elif mode == 'output':
            self.output_tokens = len(tokens)

    def cal_money(self):
        self.count_token(self.prompts_str, mode='prompt')
        self.count_token(self.output, mode='output')
        prompt_money = (self.prompt_tokens / 1000) * 0.03
        output_money = (self.output_tokens / 1000) * 0.06
        self.money = prompt_money + output_money

    def main(self):
        self.prompts_to_str()
        self.cal_money()
        self.write_money_file()