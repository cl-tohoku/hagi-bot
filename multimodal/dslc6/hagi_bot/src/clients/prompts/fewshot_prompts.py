from ..models.slots import Slot
from ..models.message import Message
from ..models.roles import Role


slot_content_fewshot_prompts = {
    Slot.CAMPUS: [
        Message(
            role=Role.USER,
            content=(
                "太郎: これはサンプルの会話です。\n"
                "次郎: サンプルです。USER の入力にはこのような形式で対話文を入れてください。"
                "複数の str に見えますが、コンマがないので 1 つの str です。"
                "(implicit string concatination)\n"
                "太郎: ここに与える会話は本番のものと内容が似ていない方がいい気がします。\n"
                "次郎: 本番の会話に誤って影響しそうですからね。\n"
                "太郎: ASSISTANT のメッセージには、この対話を見て、"
                "「会場が学内か学外か」という情報を抽出した結果を入れてください。\n"
                "次郎: この会話の場合、言及がないので「None」です。\n"
                "太郎: 言及がある場合は、その言及を入れてください。どちらの例もあるとよさそうです。\n"
                "次郎: 6つの項目について、言及がある場合とない場合の例を用意してください。\n"
                "太郎: 多分、1つ1つはこんなに長くなくていいです。\n"
                "次郎: 追加お願いします。少しでも追加したら動かしてみて、"
                "その出力が改善しているか見てみてください。\n"
                "太郎: 改善の見込みがなかったら教えて欲しいです。\n"
                "次郎: お願いします。\n"
                "太郎: 結構な数ですので、もしかしたら偽の設定を system_instructions に入れて、"
                "gpt-4 で生成するといいかもしれないですね。\n"
                "次郎: そちらの方が楽かもしれません。\n"
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
                "学内"
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
