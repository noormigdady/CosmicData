from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime as DateTime


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: DateTime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_rules(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("mission_id must start with 'M'")

        counter = 0
        for member in self.crew:
            if member.rank in {Rank.CAPTAIN, Rank.COMMANDER}:
                counter += 1
        if counter == 0:
            raise ValueError(
                "A mission must have at least one Captain or Commander"
                )

        if self.duration_days > 365:
            experienced_count = 0
            for member in self.crew:
                if member.years_experience >= 5:
                    experienced_count += 1
            if experienced_count < len(self.crew) * 0.5:
                raise ValueError(
                    "Long missions need at least 50% experienced crew members"
                    " (5+ years)"
                    )

        for member in self.crew:
            if not member.is_active:
                raise ValueError(
                    f"Crew member {member.name} is not active and cannot be "
                    "assigned to a mission"
                    )

        return self


def display_mission(mission: SpaceMission) -> None:
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${round(mission.budget_millions, 1)}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew Members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
            )
    print()


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")
    try:
        mission1 = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=DateTime(2026, 7, 20),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=20,
                    specialization="Mission Command",
                    years_experience=10,
                    is_active=True
                ),
                CrewMember(
                    member_id="C002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=25,
                    specialization="Navigation",
                    years_experience=3,
                    is_active=True
                ),
                CrewMember(
                    member_id="C003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=45,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True
                )
            ],
            budget_millions=2500.0
        )
        display_mission(mission1)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")

    print("========================================")

    try:
        mission2 = SpaceMission(
            mission_id="M2024_JUPITER",
            mission_name="Jupiter Exploration",
            destination="Jupiter",
            launch_date=DateTime(2026, 11, 20),
            duration_days=1500,
            crew=[
                CrewMember(
                    member_id="C001",
                    name="Lana Connor",
                    rank=Rank.CADET,
                    age=22,
                    specialization="Mission Command",
                    years_experience=10,
                    is_active=True
                ),
                CrewMember(
                    member_id="C002",
                    name="Jason Smith",
                    rank=Rank.LIEUTENANT,
                    age=30,
                    specialization="Navigation",
                    years_experience=3,
                    is_active=True
                ),
                CrewMember(
                    member_id="C003",
                    name="Allie Johnson",
                    rank=Rank.OFFICER,
                    age=55,
                    specialization="Engineering",
                    years_experience=6,
                    is_active=True
                )
            ],
            budget_millions=2500.0
        )
        display_mission(mission2)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")


if __name__ == "__main__":
    main()
