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
            Slot.CAMPUS: "会場が学内か学外か", # Whether the venue is on campus or off campus
            Slot.STATION: "会場が駅の近くか遠くか", # Whether the venue is near or far from the station
            Slot.PARTY: "歓迎会の規模感",   # Scale of the welcome party
            Slot.PRESENT_COST: "プレゼントの値段",  # Price of the present
            Slot.PRESENT_CONTENT: "プレゼントの内容",   # Contents of the present
            Slot.PRICE: "会費", # Participation fee
        }[self]
    
    @classmethod
    def initial_slot_contents(cls) -> dict:
        return {
            slot: None
            for slot
            in cls
        }
