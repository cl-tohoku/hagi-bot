from ..models.slots import Slot
from ..models.message import Message
from ..models.roles import Role


slot_content_fewshot_prompts = {
    Slot.CAMPUS: [
        Message(
            role=Role.USER,
            content=(
                "太郎: これはサンプルの会話です。\n"  # "Taro: This is a sample conversation."
                "次郎: サンプルです。USER の入力にはこのような形式で対話文を入れてください。" # "Jiro: It's a sample. For USER input, put the dialogue in this format."
                "複数の str に見えますが、コンマがないので 1 つの str です。" # "It looks like multiple str, but there is no comma, so it's one str."
                "(implicit string concatination)\n"  # "(implicit string concatination)"
                "太郎: ここに与える会話は本番のものと内容が似ていない方がいい気がします。\n" # "Taro: The conversation given here should not be similar to the actual one."
                "次郎: 本番の会話に誤って影響しそうですからね。\n"  # "Jiro: It seems to accidentally affect the actual conversation."
                "太郎: ASSISTANT のメッセージには、この対話を見て、"  # "Taro: For ASSISTANT's message, look at this dialogue and"
                "「会場が学内か学外か」という情報を抽出した結果を入れてください。\n"  # "put the result of extracting the information 'Is the venue on campus or off campus'."
                "次郎: この会話の場合、言及がないので「None」です。\n"  # "Jiro: In this conversation, there is no mention, so it is 'None'."
                "太郎: 言及がある場合は、その言及を入れてください。どちらの例もあるとよさそうです。\n"  # "Taro: If there is a mention, put that mention. It seems good to have both examples."
                "次郎: 6つの項目について、言及がある場合とない場合の例を用意してください。\n"  # "Jiro: Prepare examples with and without mentions for the six items."
                "太郎: 多分、1つ1つはこんなに長くなくていいです。\n"  # "Taro: Probably, it's not necessary for each one to be this long."
                "次郎: 追加お願いします。少しでも追加したら動かしてみて、"  # "Jiro: Please add more. Try running it with a little more added,"
                "その出力が改善しているか見てみてください。\n"  # "and see if the output is improving."
                "太郎: 改善の見込みがなかったら教えて欲しいです。\n"  # "Taro: If there is no prospect of improvement, please let me know."
                "次郎: お願いします。\n"  # "Jiro: Please." 
                "太郎: 結構な数ですので、もしかしたら偽の設定を system_instructions に入れて、"  # "Taro: There are quite a few, so maybe put a false setting in system_instructions,"
                "gpt-4 で生成するといいかもしれないですね。\n"  # "and it might be good to generate with gpt-4."
                "次郎: そちらの方が楽かもしれません。\n"  # "Jiro: That might be easier."
            )
        ),
        Message(
            role=Role.ASSISTANT,
            content=(
                "None"
            )
        ),
        Message(
            role=Role.USER,
            content=(
                ""
                ""
                ""
            )
        ),
        Message(
            role=Role.ASSISTANT,
            content=(
                "学内"  # "On campus"
            )
        ),
    ],
    Slot.STATION: [
    ],
    Slot.PARTY: [
    ],
    Slot.PRESENT_COST: [
    ],
    Slot.PRESENT_CONTENT: [
    ],
    Slot.PRICE: [
    ]
}


def get_fewshot_messages_counts() -> dict[Slot, int]:
    return {
        slot: len(messages)
        for slot, messages 
        in slot_content_fewshot_prompts.items()
    }
