import re
import ast
from library.aoba_profile import AobaClient
import json
# from licences_all_keys import GPT3_KEY
openai_api_key  = "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"

# jsonファイルから情報を抽出する
def extract_dicts(input_str):
    # shizuka_pattern = r'shizuka_response\s*=\s*({.*?})'
    # procedure_pattern = r'procedure_dic\s*=\s*({.*?})'

    # # shizuka_responseを取り出す
    # shizuka_match = re.search(shizuka_pattern, input_str, re.DOTALL)
    # if shizuka_match:
    #     shizuka_response_str = shizuka_match.group(1)
    #     try:
    #         shizuka_response_dict = ast.literal_eval(shizuka_response_str)
    #     except SyntaxError as e:
    #         print(f"SyntaxError in shizuka_response: {e}")
    #         shizuka_response_dict = {}
    # else:
    #     shizuka_response_dict = {}

    # # procedure_dicを取り出す
    # procedure_match = re.search(procedure_pattern, input_str, re.DOTALL)
    # if procedure_match:
    #     procedure_dic_str = procedure_match.group(1)
    #     try:
    #         procedure_dic_dict = ast.literal_eval(procedure_dic_str)
    #     except SyntaxError as e:
    #         print(f"SyntaxError in procedure_dic: {e}")
    #         procedure_dic_dict = {}
    # else:
    #     procedure_dic_dict = {}
    # return shizuka_response_dict, procedure_dic_dict
    # print(input_str)

    # GPT4の出力をjson形式で読み込む
    try:
        data = json.loads(input_str)
        # print('||||||||||||||||||||||||||||||')
        # print(data)
    except:
        print('json形式のエラー')
        print(input_str)
        return {}, {}, True

    shizuka_response_dict = data['shizuka_response']
    procedure_dic_dict = data['procedure_dic']
    return shizuka_response_dict, procedure_dic_dict, False

# 与えられた文字列
# input_str = 'shizuka_response = {\'res\': "次は会場が駅の近くかどうか、歓迎会の規模感、プレゼントの値段と内容、それに会費を決めなあかんで。", \'emotion\': "normal"}\n\nprocedure_dic={\'campus\': \'学外\',\'station\': None,\'party\': None,\'present_cost\': None,\'present_content\': None, \'price\': None}'


# 外部から関数呼び出しをするとき用（ユウキの発言を入力とする）
def get_shizuka_response(yuki_uttr):
    shizuka = AobaClient(openai_api_key)

    # １対話目
    # user_content = "そろそろ準備しないとね"
    # print("ユウキ入力:", user_content)
    # res = shizuka.get_response(user_content)
    # shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)
    
    # エラーが起きた場合の生成やり直し処理
    # while error_flag == True:
    #     shizuka.error_pop2() # 一往復文の履歴を消去
    #     res = shizuka.get_response(user_content)
    #     shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)

    # 結果の表示（デバッグ用）
    # print("res: ",res)
    # print("shizuka_response_dict: ", shizuka_response_dict)
    # print("procedure_dic_dict: ", procedure_dic_dict)

    # シズカの応答を返す（本番用）
    # shizuka_response = f'シズカ出力: {shizuka_response_dict["res"]}'
    # print(shizuka_response)

    while True:
        # user_content = input("ユウキ入力: ")
        user_content = yuki_uttr
        
        # ユーザーが "bye" と入力したらループを抜けます
        if user_content == "bye":
            print("system: さようなら、また話すのを楽しみにしています。")
            break

        # ユーザが "del" と入力したら一往復文の対話履歴を消去する
        elif user_content == "del":
            print('system: 対話をひとつもどります')
            shizuka.error_pop2()
            shizuka_res = json.loads(shizuka.messages[-1]['content'])
            print(shizuka_res['shizuka_response']['res']) # １つ前のエリカの発言を出力

        # 普通の対話のとき
        else:
            res = shizuka.get_response(user_content)
            # 辞書を抽出する関数を呼び出し
            shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)

            # エラーが起きた場合の生成やり直し処理
            while error_flag == True:
                shizuka.error_pop2() # 一往復文の履歴を消去
                res = shizuka.get_response(user_content)
                shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)
            
            # 出力の確認（デバッグ用）
            print("res: ", res)
            # print("shizuka_response_dict: ", shizuka_response_dict)
            # print("procedure_dic_dict: ", procedure_dic_dict)

            # シズカの応答を返す（本番の出力確認用）
            # shizuka_response = f'シズカ出力: {shizuka_response_dict["res"]}'
            # print(shizuka_response)

            # シズカの応答を外部に返す
            shizuka_response = shizuka_response_dict["res"]
            return shizuka_response


# このファイルを実行したときに動かすところ
if __name__ == "__main__":
    shizuka = AobaClient(openai_api_key)
    user_content = "そろそろ準備しないとね"
    print("ユウキ入力:", user_content)
    res = shizuka.get_response(user_content)
    # シズカの１文目を指定しておく，と思ったけど大丈夫そうなのでやめた
    # res = 'そうやねん、時間があっという間に過ぎていくから、早めに決めておきたいんや。それで、会場はどうする？学内にするか、それとも学外にするか？'
    shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)
    
    # エラーが起きた場合の生成やり直し処理
    while error_flag == True:
        shizuka.error_pop2() # 一往復文の履歴を消去
        res = shizuka.get_response(user_content)
        shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)

    # 結果の表示（デバッグ用）
    print("res: ",res)
    # print("shizuka_response_dict: ", shizuka_response_dict)
    # print("procedure_dic_dict: ", procedure_dic_dict)

    # シズカの応答を返す（本番用）
    # shizuka_response = f'シズカ出力: {shizuka_response_dict["res"]}'
    # print(shizuka_response)

    while True:
        user_content = input("ユウキ入力: ")
        
        # ユーザーが "bye" と入力したらループを抜けます
        if user_content == "bye":
            print("system: さようなら、また話すのを楽しみにしています。")
            break

        # ユーザが "del" と入力したら一往復文の対話履歴を消去する
        elif user_content == "del":
            print('system: 対話をひとつもどります')
            shizuka.error_pop2()
            shizuka_res = json.loads(shizuka.messages[-1]['content'])
            print(shizuka_res['shizuka_response']['res']) # １つ前のエリカの発言を出力

        # 普通の対話のとき
        else:
            res = shizuka.get_response(user_content)
            # 辞書を抽出する関数を呼び出し
            shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)

            # エラーが起きた場合の生成やり直し処理
            while error_flag == True:
                shizuka.error_pop2() # 一往復文の履歴を消去
                res = shizuka.get_response(user_content)
                shizuka_response_dict, procedure_dic_dict, error_flag = extract_dicts(res)
            
            # 出力の確認（デバッグ用）
            print("res: ", res)
            # print("shizuka_response_dict: ", shizuka_response_dict)
            # print("procedure_dic_dict: ", procedure_dic_dict)

            # シズカの応答を返す（本番用）
            # shizuka_response = f'シズカ出力: {shizuka_response_dict["res"]}'
            # print(shizuka_response)