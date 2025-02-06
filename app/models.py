# Standard Imports
from datetime import time as dtime
from pydantic import BaseModel
from typing import Dict


class Restaurant(BaseModel):
    id: int
    latitude: float
    longitude: float
    availability_radius: float  # in km
    open_hour: dtime
    close_hour: dtime
    rating: float

    @classmethod
    def from_csv_row(cls, row: Dict[str, str]) -> "Restaurant":
        # Parse ISO formatted times using datetime.time.fromisoformat()
        open_dt = dtime.fromisoformat(row["open_hour"])
        close_dt = dtime.fromisoformat(row["close_hour"])
        
        return cls(
            id=int(row["id"]),
            latitude=float(row["latitude"]),
            longitude=float(row["longitude"]),
            availability_radius=float(row["availability_radius"]),
            open_hour=open_dt,
            close_hour=close_dt,
            rating=float(row["rating"]),
        )
