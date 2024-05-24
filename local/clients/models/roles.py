from enum import Enum


class Role(Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

    @property
    def main_character_name(self) -> str:
        if self == Role.SYSTEM:
            raise ValueError("SYSTEM role has no character name.")
        return {
            Role.USER: "ユウキ",  # Yuki
            Role.ASSISTANT: "シズカ"  # Shizuka
        }[self]
