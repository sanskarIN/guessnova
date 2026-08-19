"""User-facing settings."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(slots=True)
class Settings:
    theme: str = "nebula"
    reduced_motion: bool = False
    high_contrast: bool = False
    sound: bool = False
    show_smart_hints: bool = True

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> "Settings":
        allowed = {field: data[field] for field in asdict(cls()).keys() if field in data}
        return cls(**allowed)  # type: ignore[arg-type]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
