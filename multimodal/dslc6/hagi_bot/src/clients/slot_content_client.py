from .slot_client import SlotClient
from .prompts.system_instructions import slot_content_instruction_template
from .models.slots import Slot
from .models.config import ModelConfig
from .prompts.fewshot_prompts import slot_content_fewshot_prompts
from .models.message import Message


class SlotContentClient(SlotClient):

    def __init__(
            self, 
            *,
            model_config: ModelConfig,
            slot: Slot, 
            input_history_length: int | None = None
            ) -> None:
        super().__init__(
            model_config=model_config, 
            input_history_length=input_history_length
        )
        self.load_system_instruction()
        self.slot = slot

    def load_system_instruction(self) -> None:
        self.system_instruction_template = slot_content_instruction_template

    @property
    def specific_instruction(self) -> str:
        if self.slot == Slot.STATION:
            # If on campus, near a train station
            f"{Slot.STATION.text}が学内に決まった場合は、会場は駅近の近くに決まったものとしてください。"  # If {Slot.STATION.text} is decided on campus, the venue is decided near the station.
        return ""

    @property
    def system_instruction(self) -> str:
        return self.system_instruction_template.format(slot=self.slot.text, specific_instruction=self.specific_instruction)
    
    @property
    def is_conversation_done(self) -> bool:
        is_done = "None" not in self.last_assistant_response
        return is_done
    
    @property
    def slot_content(self) -> str | None:
        if self.is_conversation_done:
            return self.last_assistant_response
        else:
            return None

    def add_main_chat_history_as_user_input(
            self, 
            *, 
            main_chat_history: list[Message],
            enable_fewshot: bool = True
            ) -> None:
        self.update_main_history(main_chat_history)
        chat_history_text = self.chat_history_text
        self.add_user_input(chat_history_text)
        fewshot_prompts = slot_content_fewshot_prompts[self.slot]
        if enable_fewshot:
            self.concat_fewshot_messages(fewshot_prompts)
