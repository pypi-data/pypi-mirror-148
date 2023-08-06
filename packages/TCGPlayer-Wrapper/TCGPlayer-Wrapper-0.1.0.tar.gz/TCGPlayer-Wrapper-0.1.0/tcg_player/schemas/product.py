from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Any, Dict

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Product:
    product_id: int
    name: str
    clean_name: str
    image_url: str
    category_id: int
    group_id: int
    url: str
    modified_on: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Product":
        try:
            if "." in (modified_on := str(data.pop("modifiedOn"))):
                modified_on = modified_on[: modified_on.rindex(".")]
            obj = cls(
                product_id=int(data.pop("productId")),
                name=str(data.pop("name")),
                clean_name=str(data.pop("cleanName")),
                image_url=str(data.pop("imageUrl")),
                category_id=int(data.pop("categoryId")),
                group_id=int(data.pop("groupId")),
                url=str(data.pop("url")),
                modified_on=datetime.fromisoformat(modified_on),
            )
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
