from dataclasses import asdict, dataclass
from typing import Optional


@dataclass
class Location:
    city: str
    country: str
    latitude: float
    longitude: float
    timezone: str = ""


@dataclass
class AirQualityRecord:
    city: str
    country: str
    time: str
    pm25: Optional[float]
    pm10: Optional[float]
    carbon_monoxide: Optional[float]
    nitrogen_dioxide: Optional[float]
    sulphur_dioxide: Optional[float]
    ozone: Optional[float]
    uv_index: Optional[float]
    risk_level: str = "Unknown"
    recommendation: str = "No recommendation available."

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(
            city=data.get("city", "Unknown"),
            country=data.get("country", "Unknown"),
            time=data.get("time", ""),
            pm25=data.get("pm25"),
            pm10=data.get("pm10"),
            carbon_monoxide=data.get("carbon_monoxide"),
            nitrogen_dioxide=data.get("nitrogen_dioxide"),
            sulphur_dioxide=data.get("sulphur_dioxide"),
            ozone=data.get("ozone"),
            uv_index=data.get("uv_index"),
            risk_level=data.get("risk_level", "Unknown"),
            recommendation=data.get(
                "recommendation",
                "No recommendation available.",
            ),
        )