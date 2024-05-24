import openai
from typing import Generator
import re
from itertools import zip_longest
import asyncio
from threading import Timer, Event
from timeout_decorator import timeout
from itertools import chain
from openai.error import Timeout

from .config import ModelConfig
from .message import Message
from .roles import Role
# from ...utils import ManageMoney

import copy # 追加

class OpenAIChat:

    def __init__(self, *, model_config: ModelConfig) -> None:
        self.model = model_config.model
        self.history_length = model_config.history_length
        self.max_tokens = model_config.max_tokens
        self.temperature = model_config.temperature
        self.top_p = model_config.top_p
        self.frequency_penalty = model_config.frequency_penalty
        self.presence_penalty = model_config.presence_penalty
        self.chat_history: list[Message] = list()
        self.timeout = model_config.timeout
        self.max_retry = model_config.max_retry
        self.logit_bias = model_config.logit_bias

    def add_message(self, message: Message) -> None:
        self.chat_history.append(message)
        if self.history_length is not None:
            self.chat_history = self.chat_history[-self.history_length:]
        elif self.history_length == 0:
            self.chat_history = list()

    def concat_fewshot_messages(self, fewshot_messages: list[Message]) -> None:
        """
        Note: This method must be called after `add_message`.
        - Because `add_message` truncates the `chat_history` according to the `history_length`, the
        """
        self.chat_history = fewshot_messages + self.chat_history

    def add_user_input(self, content: str) -> None:
        self.add_message(Message(Role.USER, content))

    def add_assistant_response(self, content: str) -> None:
        self.add_message(Message(Role.ASSISTANT, content))

    @property
    def messages(self) -> list[dict[str, str]]:
        messages = [Message(Role.SYSTEM, self.system_instruction).to_dict()]
        for message in self.chat_history:
            messages.append(message.to_dict())
        return messages

    async def request_assistant_response(self) -> None:
        result = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=self.messages,
            max_tokens=self.max_tokens,
            temperature=self.temperature,
            top_p=self.top_p,
            frequency_penalty=self.frequency_penalty,
            presence_penalty=self.presence_penalty,
            logit_bias=self.logit_bias
        )
        content = result.choices[0].message.content
        self.add_assistant_response(content)

    def debug_print(self, message: str) -> None:
        GRAY = "\033[90m"
        RESET = "\033[0m"
        print(f"{GRAY}[MODEL DEBUG] {message}{RESET}")

    async def request_assistant_response_with_retry(self) -> None:

        n_retry = 0

        while True:
            try:
                if self.max_retry is None or n_retry < self.max_retry:
                    await asyncio.wait_for(
                        self.request_assistant_response(), 
                        timeout=self.timeout
                        )
                else:
                    self.debug_print(f"(async) max_retry exceeded. waiting for the last api request...")
                    await self.request_assistant_response()
                break
            except asyncio.TimeoutError:
                self.debug_print("(async) api timeout. retrying...")
                n_retry += 1
                continue

    @property
    def last_assistant_response(self) -> str:
        try:
            last_message = self.chat_history[-1]
        except IndexError:
            raise IndexError("No assistant response yet.")
        if last_message.role == Role.ASSISTANT:
            return last_message.content
        else:
            raise IndexError("No assistant response yet.")
        
    def print_last_assistant_response(self) -> None:
        print(self.last_assistant_response)

    def request_and_print_assistant_response(self) -> None:
        asyncio.run(self.request_assistant_response_with_retry())
        self.print_last_assistant_response()
    
    def request_assistant_response_stream(self) -> Generator[str, None, None]:
        '''
        Putting the money management module in here.
        '''
        # self._result = None

        # def create_timeoutable() -> Generator:
        #     self._result = openai.ChatCompletion.create(
        #         model=self.model,
        #         messages=self.messages,
        #         max_tokens=self.max_tokens,
        #         temperature=self.temperature,
        #         top_p=self.top_p,
        #         frequency_penalty=self.frequency_penalty,
        #         presence_penalty=self.presence_penalty,
        #         stream=True,
        #         logit_bias=self.logit_bias
        #     )
        #     first_chunk = next(self._result)      # 最初の 2 応答が返ってくるまで待つ
        #     # self.debug_print(f"first_chunk: {first_chunk}")
        #     second_chunk = next(self._result)
        #     # self.debug_print(f"second_chunk: {second_chunk}")
        #     result = chain([first_chunk, second_chunk], self._result)
        #     return result

        # @timeout(self.timeout, timeout_exception=TimeoutError)
        # def create_with_timeout():
        #     return create_timeoutable()

        # def create_without_timeout():
        #     return create_timeoutable()

        n_retry = 0
        while True:
            
            try:
                # # WIP: メインモデルのタイムアウト
                # if self.max_retry is None or n_retry < self.max_retry:
                #     result = create_with_timeout()
                # else:
                #     self.debug_print(f"(stream) max_retry exceeded. waiting for the last api request...")
                #     result = create_without_timeout()
                # result = create_without_timeout()
                params = dict(
                    model=self.model,
                    messages=self.messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    frequency_penalty=self.frequency_penalty,
                    presence_penalty=self.presence_penalty,
                    stream=True,
                    logit_bias=self.logit_bias,
                )

                if self.max_retry is None or n_retry < self.max_retry:
                    params["request_timeout"] = self.timeout
                else:
                    self.debug_print(f"(stream) max_retry exceeded. waiting for the last api request...")

                result = openai.ChatCompletion.create(
                    **params
                )

                total_content = ""
                for chunk in result:
                    delta = chunk.choices[0].delta
                    if delta:
                        content = chunk.choices[0].delta.content
                        total_content += content
                        yield content

                break

            except Timeout:
                self.debug_print(f"(stream) api timeout. retrying...")
                n_retry += 1
                continue

        # print(self.messages) # debug
        # monege_money = ManageMoney(prompt=self.messages, output=total_content, file_path=manage_money.csv)
        # monege_money.money()
        self.add_assistant_response(total_content)

    def _split_with_delimiters(self, content: str, delimiter_pattern: str) -> list[str]:
        split_content = re.split(delimiter_pattern, content)
        return [
            content + delimiter
            for content, delimiter
            in zip_longest(split_content[::2], split_content[1::2], fillvalue="")
        ]

    def request_and_print_assistant_response_stream(
            self, 
            stream_delimiters: list[str] = ["、", "。", "？", "！", "…"]
            ):
        
        delimiters_pattern = re.compile(f"({'|'.join(f'{delimiter}+' for delimiter in stream_delimiters)})")

        sentence = ""
        for content in self.request_assistant_response_stream():
            split_contents = self._split_with_delimiters(content, delimiters_pattern)
            continuation, *sentences = split_contents
            if not sentences:
                sentence += continuation
                continue
            sentence += continuation
            # print(f"{sentence}")

            result_sentence = copy.deepcopy(sentence)
            sentence = ""
            for sentence in sentences[:-1]:
                print(f"{sentence}")
                print("||||||||||||||||||||||||||||||||||||||||||||||||||")
            sentence = sentences[-1]

            yield result_sentence