from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional

from tcg_player.schemas.exceptions import ValidationError


@dataclass
class Price:
    product_id: int
    low_price: Optional[float]
    mid_price: Optional[float]
    high_price: Optional[float]
    market_price: Optional[float]
    direct_low_price: Optional[float]
    sub_type_name: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Price":
        try:
            obj = cls(
                product_id=int(data.pop("productId")),
                low_price=float(data.pop("lowPrice")) if data["lowPrice"] else None,
                mid_price=float(data.pop("midPrice")) if data["midPrice"] else None,
                high_price=float(data.pop("highPrice")) if data["highPrice"] else None,
                market_price=float(data.pop("marketPrice")) if data["marketPrice"] else None,
                direct_low_price=float(data.pop("directLowPrice"))
                if data["directLowPrice"]
                else None,
                sub_type_name=str(data.pop("subTypeName")),
            )
            if "lowPrice" in data:
                del data["lowPrice"]
            if "midPrice" in data:
                del data["midPrice"]
            if "highPrice" in data:
                del data["highPrice"]
            if "marketPrice" in data:
                del data["marketPrice"]
            if "directLowPrice" in data:
                del data["directLowPrice"]
        except (TypeError, KeyError) as err:
            raise ValidationError(f"Invalid Key: {err}")
        if data:
            raise ValidationError(f"Missed Keys: {list(data.keys())}")
        return obj

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
