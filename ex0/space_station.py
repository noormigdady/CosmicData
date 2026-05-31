from pydantic import BaseModel, Field, ValidationError
from datetime import datetime as DateTime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: DateTime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def display_station(station: SpaceStation) -> None:
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    status = "Operational" if station.is_operational else "Not Operational"
    print(f"Operational Status: {status}")


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        station1 = SpaceStation(
            station_id=" ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=DateTime(2024, 5, 20, 14, 30),
            is_operational=True,
        )
        display_station(station1)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")

    print("\n========================================")

    try:
        station2 = SpaceStation(
            station_id="SS002",
            name="Lunar Gateway",
            crew_size=22,
            power_level=75.0,
            oxygen_level=88.0,
            last_maintenance=DateTime(2024, 6, 15, 10, 0),
            is_operational=False,
            notes="Scheduled for maintenance in July."
        )
        display_station(station2)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")


if __name__ == "__main__":
    main()
