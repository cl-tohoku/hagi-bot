import openai
import os
import argparse
import asyncio
import time
import tiktoken

from clients.models.config import ModelConfig
from clients.main_client import MainClient
from clients.slot_content_client import SlotContentClient
from clients.models.slots import Slot
from clients.prompts.fewshot_prompts import slot_content_fewshot_prompts, get_fewshot_messages_counts


async def await_all(objects: list) -> list:
    return await asyncio.gather(*objects)


def debug_print(args, message: str) -> None:
    if args.debug:
        GRAY = "\033[90m"
        RESET = "\033[0m"
        print(f"{GRAY}[DEBUG] {message}{RESET}")


def warn_print(args, message: str) -> None:
    if args.debug:
        if not args.disable_warning:
            YELLOW = "\033[33m"
            RESET = "\033[0m"
            print(f"{YELLOW}[WARNING] {message}{RESET}")


def main(args) -> None:
    openai.api_key = os.getenv("OPENAI_API_KEY")

    # Settings of main model
    main_model_config = ModelConfig(
        model=args.main_model, 
        history_length=args.main_histrory_length,
        frequency_penalty=0.2,
    )

    # Create client of main model
    main_client = MainClient(model_config=main_model_config)

    # Settings of slot model
    # give 1 conversation, so history_length=1 (if you want to give n conversations, history_length=2n-1)
    slot_model_config = ModelConfig(
        model=args.slot_model, 
        history_length=1,
        max_tokens=32,
    )

    # Create client of slot model
    slot_clients = {
        slot: SlotContentClient(
            model_config=slot_model_config,
            slot=slot,
            input_history_length=args.slot_input_histrory_length
        ) 
        for slot 
        in Slot
    }

    # Start conversation
    while True:
        # Receive user input
        uttr = input("ユウキ: ")
        user_content = uttr

        # メインモデルの応答時間の計測開始
        start_time = time.time()

        # ユーザが "q" あるいは "exit" と入力したらループを抜ける (DEBUG)
        if args.debug:
            if user_content in ["exit", "q"]:
                break

        # ユーザの入力をメインモデルに渡す
        main_client.add_user_input(user_content)

        # メインモデルの応答を要求し、応答を出力する
        debug_print(args, "メインモデルへのリクエスト開始")
        if args.stream:
            for sentence in main_client.request_and_print_assistant_response_stream():
                print(f"シズカ: {sentence}")

        else:
            main_client.request_and_print_assistant_response()

        # メインモデルの応答時間の計測終了
        end_time = time.time()
        elapsed_time = end_time - start_time

        # メインモデルの応答時間を出力する (DEBUG)
        debug_print(args, f"elapsed_time: {elapsed_time:.2f} sec")

        # スロットコンテンツモデルの応答時間の計測開始
        start_time = time.time()

        # スロットコンテンツモデルに渡す対話履歴を取得する
        main_chat_history = main_client.chat_history

        # スロットコンテンツモデルに渡す対話履歴を出力する (DEBUG)
        # debug_print(args, f"main_chat_history: {main_chat_history}")

        # メインモデルの対話履歴をスロットコンテンツモデルに渡す
        for slot in Slot:
            # スロットコンテンツモデルに最新の対話履歴を入力として渡す
            slot_clients[slot].add_main_chat_history_as_user_input(
                main_chat_history=main_chat_history,
                enable_fewshot=args.enable_fewshot
            )

        # スロットコンテンツモデルの応答を要求する
        debug_print(args, "スロットモデルへのリクエスト開始")
        asyncio.run(
            await_all(
                [
                    slot_client.request_assistant_response()
                    for slot_client
                    in slot_clients.values()
                ]
            )
        )

        # スロットコンテンツモデルの応答を受け取る
        slot_contents = {
            slot: slot_client.slot_content
            for slot, slot_client
            in slot_clients.items()
        }

        # スロットコンテンツモデルの応答時間の計測終了
        end_time = time.time()
        elapsed_time = end_time - start_time

        # スロットコンテンツモデルの応答時間を出力する (DEBUG)
        debug_print(args, f"elapsed_time: {elapsed_time:.2f} sec")

        # スロットコンテンツモデルの応答を出力する (DEBUG)
        slot_contents_str = ", ".join([f"{slot.text}: {content}" for slot, content in slot_contents.items()])
        debug_print(args, f"slot_contents: {{{slot_contents_str}}}")

        # メインモデルの保持するスロットコンテンツを更新する
        main_client.slot_contents = slot_contents

# --stream の default をstreamモードにしたので、引数で指定する必要なし（指定するとむしろstreamモードじゃ無くなる）
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--main-model", type=str, default="gpt-3.5-turbo")  # default はGPT3.5
    parser.add_argument("--slot-model", type=str, default="gpt-3.5-turbo")  # default はGPT3.5
    parser.add_argument("--main-histrory-length", type=int, default=None)
    parser.add_argument("--slot-input-histrory-length", type=int, default=None)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--disable-warning", action="store_true")
    parser.add_argument("--enable-fewshot", action="store_true")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--max_time", type=float, default=290.0) # 制限時間の追加
    parser.add_argument("--time_out", type=float, default=2.0) # user input のタイムアウト追加
    parser.add_argument("--is_time_out", action="store_false") # user input のタイムアウトのスイッチ
    parser.add_argument("--main-model-timeout", type=float, default=10)
    parser.add_argument("--slot-model-timeout", type=float, default=10)
    parser.add_argument("--main-model-max-retry", type=int, default=5)
    parser.add_argument("--slot-model-max-retry", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=256)
    # parser.add_argument("--ending-bias", type=int, default=10)  # 出力を短くしますが、API 側のバグで利用できません。

    args = parser.parse_args()

    if args.main_model != "gpt-4":
        warn_print(args, "gpt-4 以前のモデルでは表情が変化しない可能性があります。")
    if args.slot_model != "gpt-4":
        warn_print(args, "gpt-4 以前のモデルではスロットの出力が安定しません。安定には few-shot prompt の追加が必要です。")
        if args.enable_fewshot:
            counts = get_fewshot_messages_counts()
            counts_str = ", ".join([f"{slot.text}: {count}件" for slot, count in counts.items()])
            count_sum = sum(counts.values())
            warn_print(args, f"現在登録されている few-shot の対話文は {counts_str} の計{count_sum}件です。")
        else:
            warn_print(args, "few-shot prompt を有効にするには `--enable-fewshot` を指定してください。")

    return args


if __name__ == "__main__":
    args = get_args()
    main(args)