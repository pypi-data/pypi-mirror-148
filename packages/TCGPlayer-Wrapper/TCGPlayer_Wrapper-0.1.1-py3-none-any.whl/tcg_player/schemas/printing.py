from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Printing:
    printing_id: int
    name: str
    display_order: int
    modified_on: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Printing":
        try:
            if "." in (modified_on := str(data.pop("modifiedOn"))):
                modified_on = modified_on[: modified_on.rindex(".")]
            obj = cls(
                printing_id=int(data.pop("printingId")),
                name=str(data.pop("name")),
                display_order=int(data.pop("displayOrder")),
                modified_on=datetime.fromisoformat(modified_on),
            )
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
