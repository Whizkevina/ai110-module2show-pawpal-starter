from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str
    category: str = "general"
    pet: Pet | None = None
    completed: bool = False
    completion_timestamp: str = ""
    skipped_reason: str = ""

    def priority_score(self, owner: Owner) -> int:
        raise NotImplementedError

    def can_fit(self, available_minutes: int) -> bool:
        raise NotImplementedError


@dataclass
class Pet:
    name: str
    species: str
    age_years: int = 0
    care_tasks: List[Task] = field(default_factory=list)
    care_notes: List[str] = field(default_factory=list)

    def profile_summary(self) -> str:
        raise NotImplementedError

    def add_care_note(self, note: str) -> None:
        raise NotImplementedError


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    daily_time_budget_minutes: int = 0

    def add_pet(self, pet: Pet) -> None:
        raise NotImplementedError

    def add_preference(self, preference: str) -> None:
        raise NotImplementedError

    def summary(self) -> str:
        raise NotImplementedError


class SchedulePlanner:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def collect_tasks(self) -> List[Task]:
        raise NotImplementedError

    def sort_tasks(self) -> List[Task]:
        raise NotImplementedError

    def build_plan(self) -> List[Task]:
        raise NotImplementedError

    def explain_plan(self) -> str:
        raise NotImplementedError