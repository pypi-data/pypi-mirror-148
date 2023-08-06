from dataclasses import asdict, dataclass
from typing import Any, Dict

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Language:
    language_id: int
    name: str
    abbreviation: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Language":
        try:
            obj = cls(
                language_id=int(data.pop("languageId")),
                name=str(data.pop("name")),
                abbreviation=str(data.pop("abbr")),
            )
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
