from enum import Enum


class Slot(Enum):
    CAMPUS = "campus"
    STATION = "station"
    PARTY = "party"
    PRESENT_COST = "present_cost"
    PRESENT_CONTENT = "present_content"
    PRICE = "price"

    @property
    def text(self) -> str:
        return {
            Slot.CAMPUS: "会場が学内か学外か",
            Slot.STATION: "会場が駅の近くか遠くか",
            Slot.PARTY: "歓迎会の規模感",
            Slot.PRESENT_COST: "プレゼントの値段",
            Slot.PRESENT_CONTENT: "プレゼントの内容",
            Slot.PRICE: "会費",
        }[self]
    
    @classmethod
    def initial_slot_contents(cls) -> dict:
        return {
            slot: None
            for slot
            in cls
        }
