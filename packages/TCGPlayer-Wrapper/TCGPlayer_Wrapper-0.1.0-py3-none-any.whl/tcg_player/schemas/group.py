from dataclasses import asdict, dataclass
from datetime import date, datetime
from typing import Any, Dict, Optional

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Group:
    group_id: int
    name: str
    abbreviation: Optional[str]
    is_supplemental: bool
    published_on: date
    modified_on: datetime
    category_id: int

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Group":
        try:
            if "T" in (published_on := str(data.pop("publishedOn"))):
                published_on = published_on[: published_on.index("T")]
            if "." in (modified_on := str(data.pop("modifiedOn"))):
                modified_on = modified_on[: modified_on.rindex(".")]
            obj = cls(
                group_id=int(data.pop("groupId")),
                name=str(data.pop("name")),
                abbreviation=str(data.pop("abbreviation"))
                if "abbreviation" in data and data["abbreviation"]
                else None,
                is_supplemental=data.pop("isSupplemental") is True,
                published_on=date.fromisoformat(published_on),
                modified_on=datetime.fromisoformat(modified_on),
                category_id=int(data.pop("categoryId")),
            )
            if "abbreviation" in data:
                del data["abbreviation"]
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
