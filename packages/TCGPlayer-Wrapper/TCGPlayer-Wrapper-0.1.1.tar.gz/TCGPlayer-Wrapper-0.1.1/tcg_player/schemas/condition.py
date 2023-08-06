from dataclasses import asdict, dataclass
from typing import Any, Dict

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Condition:
    condition_id: int
    name: str
    abbreviation: str
    display_order: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Condition":
        try:
            obj = cls(
                condition_id=int(data.pop("conditionId")),
                name=str(data.pop("name")),
                abbreviation=str(data.pop("abbreviation")),
                display_order=int(data.pop("displayOrder")),
            )
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
