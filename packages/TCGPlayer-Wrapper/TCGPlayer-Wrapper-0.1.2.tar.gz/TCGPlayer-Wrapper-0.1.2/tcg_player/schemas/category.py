from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict, Optional

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Category:
    category_id: int
    name: str
    modified_on: datetime
    display_name: str
    seo_category_name: str
    sealed_label: Optional[str]
    non_sealed_label: Optional[str]
    condition_guide_url: str
    is_scannable: bool
    popularity: int
    is_direct: bool

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Category":
        try:
            if "." in (modified_on := str(data.pop("modifiedOn"))):
                modified_on = modified_on[: modified_on.rindex(".")]
            obj = cls(
                category_id=int(data.pop("categoryId")),
                name=str(data.pop("name")),
                modified_on=datetime.fromisoformat(modified_on),
                display_name=str(data.pop("displayName")),
                seo_category_name=str(data.pop("seoCategoryName")),
                sealed_label=str(data.pop("sealedLabel"))
                if "sealedLabel" in data and data["sealedLabel"]
                else None,
                non_sealed_label=str(data.pop("nonSealedLabel"))
                if "nonSealedLabel" in data and data["nonSealedLabel"]
                else None,
                condition_guide_url=str(data.pop("conditionGuideUrl")),
                is_scannable=data.pop("isScannable") is True,
                popularity=int(data.pop("popularity")),
                is_direct=data.pop("isDirect") is True,
            )
            if "sealedLabel" in data:
                del data["sealedLabel"]
            if "nonSealedLabel" in data:
                del data["nonSealedLabel"]
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
