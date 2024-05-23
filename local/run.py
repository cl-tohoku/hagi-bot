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

        # Start measuring the response time of the main model
        start_time = time.time()

        # Exit the loop when the user inputs "q" or "exit" (DEBUG)
        if args.debug:
            if user_content in ["exit", "q"]:
                break

        # Pass user input to the main model
        main_client.add_user_input(user_content)

        # Requests a response from the main model and outputs a response
        debug_print(args, "メインモデルへのリクエスト開始")  # "Start of request to main model"
        if args.stream:
            for sentence in main_client.request_and_print_assistant_response_stream():
                print(f"シズカ: {sentence}")  # "Shizuka:"

        else:
            main_client.request_and_print_assistant_response()

        # End of main model response time measurement
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Output main model response time (DEBUG)
        debug_print(args, f"elapsed_time: {elapsed_time:.2f} sec")

        # Start measuring the response time of the slot content model
        start_time = time.time()

        # Obtain dialogue history to be passed to the slot content model
        main_chat_history = main_client.chat_history

        # Output dialogue history to be passed to the slot content model (DEBUG)
        # debug_print(args, f"main_chat_history: {main_chat_history}")

        # Passing the dialogue history of the main model to the slot content model
        for slot in Slot:
            # Passing the latest dialogue history as input to the slot content model
            slot_clients[slot].add_main_chat_history_as_user_input(
                main_chat_history=main_chat_history,
                enable_fewshot=args.enable_fewshot
            )

        # Request response to slot content model.
        debug_print(args, "スロットモデルへのリクエスト開始") # "Start of request to slot model"
        asyncio.run(
            await_all(
                [
                    slot_client.request_assistant_response()
                    for slot_client
                    in slot_clients.values()
                ]
            )
        )

        # Receive slot content model response
        slot_contents = {
            slot: slot_client.slot_content
            for slot, slot_client
            in slot_clients.items()
        }

        # End of measurement of response times for slot content models
        end_time = time.time()
        elapsed_time = end_time - start_time

        # Output response time of slot content model (DEBUG)
        debug_print(args, f"elapsed_time: {elapsed_time:.2f} sec")

        # Output slot content model response (DEBUG)
        slot_contents_str = ", ".join([f"{slot.text}: {content}" for slot, content in slot_contents.items()])
        debug_print(args, f"slot_contents: {{{slot_contents_str}}}")

        # Update slot content held by the main model.
        main_client.slot_contents = slot_contents


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--main-model", type=str, default="gpt-3.5-turbo")  # default: GPT3.5
    parser.add_argument("--slot-model", type=str, default="gpt-3.5-turbo")  # default: GPT3.5
    parser.add_argument("--main-histrory-length", type=int, default=None)
    parser.add_argument("--slot-input-histrory-length", type=int, default=None)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--disable-warning", action="store_true")
    parser.add_argument("--enable-fewshot", action="store_true")
    parser.add_argument("--stream", action="store_true")
    parser.add_argument("--max_time", type=float, default=290.0) # add max time
    parser.add_argument("--time_out", type=float, default=2.0) # add user input time out
    parser.add_argument("--is_time_out", action="store_false") # add user input time out switch
    parser.add_argument("--main-model-timeout", type=float, default=10)
    parser.add_argument("--slot-model-timeout", type=float, default=10)
    parser.add_argument("--main-model-max-retry", type=int, default=5)
    parser.add_argument("--slot-model-max-retry", type=int, default=3)
    parser.add_argument("--max-tokens", type=int, default=256)
    # parser.add_argument("--ending-bias", type=int, default=10)  # Shortens the output, but is not available due to a bug on the API side

    args = parser.parse_args()

    if args.main_model != "gpt-4":
        warn_print(args, "gpt-4 以前のモデルでは表情が変化しない可能性があります。")  # "Models before gpt-4 may not change facial expressions."
    if args.slot_model != "gpt-4":
        warn_print(args, "gpt-4 以前のモデルではスロットの出力が安定しません。安定には few-shot prompt の追加が必要です。")  # "Models before gpt-4 may not stabilize the output of the slot. Adding a few-shot prompt is necessary for stabilization."
        if args.enable_fewshot:
            counts = get_fewshot_messages_counts()
            counts_str = ", ".join([f"{slot.text}: {count}件" for slot, count in counts.items()])
            count_sum = sum(counts.values())
            warn_print(args, f"現在登録されている few-shot の対話文は {counts_str} の計{count_sum}件です。")  # "The number of registered few-shot dialogues is currently {counts_str}, totaling {count_sum}."
        else:
            warn_print(args, "few-shot prompt を有効にするには `--enable-fewshot` を指定してください。")  # "To enable few-shot prompt, specify `--enable-fewshot`."

    return args


if __name__ == "__main__":
    args = get_args()
    main(args)