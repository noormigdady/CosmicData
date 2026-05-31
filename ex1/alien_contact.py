from pydantic import BaseModel, Field, ValidationError, model_validator
from enum import Enum
from datetime import datetime as DateTime
from typing import Optional


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: DateTime
    location: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must start with 'AC'")
        if self.contact_type == ContactType.PHYSICAL and not self.is_verified:
            raise ValueError("Physical contact reports must be verified")
        if (
            self.contact_type == ContactType.TELEPATHIC and
                self.witness_count < 3
                ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
                )
        if self.signal_strength > 7 and not self.message_received:
            raise ValueError(
                "Strong signals > 7 should include received message"
                )
        return self


def display_contact(alien: AlienContact) -> None:
    print("Valid contact report:")
    print(f"ID: {alien.contact_id}")
    print(f"Type: {alien.contact_type.value}")
    print(f"Location: {alien.location}")
    print(f"Signal: {alien.signal_strength} / 10")
    print(f"Duration: {alien.duration_minutes} minutes")
    print(f"Witness: {alien.witness_count}")
    if alien.message_received:
        print(f"Message: {alien.message_received}")


def main() -> None:
    print("Alien Contact Data Validation")
    print("========================================")
    try:
        contact1 = AlienContact(
            contact_id="AC_2024_001",
            timestamp=DateTime(2024, 6, 1, 12, 0),
            location=" Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli",
            is_verified=True,
        )
        display_contact(contact1)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")

    print("\n========================================")

    try:
        contact2 = AlienContact(
            contact_id="AC54321",
            timestamp=DateTime(2024, 6, 2, 15, 30),
            location="Sector 9B",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=0.0,
            duration_minutes=10,
            witness_count=0,
            is_verified=False,
        )
        display_contact(contact2)

    except ValidationError as e:
        for error in e.errors():
            print(f"Expected validation error:"
                  f" {error['msg'].removeprefix("Value error,")}")


if __name__ == "__main__":
    main()
