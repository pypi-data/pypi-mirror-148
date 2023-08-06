from dataclasses import asdict, dataclass
from typing import Any, Dict

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Rarity:
    rarity_id: int
    display_text: str
    db_value: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Rarity":
        try:
            obj = cls(
                rarity_id=int(data.pop("rarityId")),
                display_text=str(data.pop("displayText")),
                db_value=str(data.pop("dbValue")),
            )
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
