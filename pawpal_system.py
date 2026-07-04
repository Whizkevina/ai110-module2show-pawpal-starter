from __future__ import annotations

from datetime import datetime
from dataclasses import dataclass, field
from typing import List


PRIORITY_RANKS = {"high": 0, "medium": 1, "low": 2}


def _parse_time_label(time_label: str) -> tuple[int, int]:
    if not time_label:
        return (99, 59)

    hours, minutes = time_label.split(":", maxsplit=1)
    return (int(hours), int(minutes))


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str = "daily"
    priority: str = "medium"
    preferred_time: str = ""
    pet: Pet | None = None
    completed: bool = False
    completion_timestamp: str = ""
    skipped_reason: str = ""

    def mark_complete(self) -> None:
        """Mark this task as complete."""
        self.completed = True
        self.skipped_reason = ""
        self.completion_timestamp = datetime.now().isoformat(timespec="seconds")

    def priority_score(self, owner: Owner | None = None) -> int:
        """Return a higher score for higher-priority tasks."""
        score = 100 - PRIORITY_RANKS.get(self.priority.lower(), 3) * 20
        if self.preferred_time:
            score += 5
        if owner and self.pet and any(preference.lower() in self.description.lower() for preference in owner.preferences):
            score += 3
        return score

    def can_fit(self, available_minutes: int) -> bool:
        """Check whether the task fits in the remaining schedule time."""
        return self.duration_minutes <= available_minutes

    def schedule_label(self) -> str:
        """Format the task for terminal output."""
        time_label = self.preferred_time or "Anytime"
        pet_label = f" for {self.pet.name}" if self.pet else ""
        return (
            f"{time_label} — {self.description}{pet_label} "
            f"({self.duration_minutes} min, priority: {self.priority})"
        )


@dataclass
class Pet:
    name: str
    species: str
    age_years: int = 0
    care_tasks: List[Task] = field(default_factory=list)
    care_notes: List[str] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet."""
        task.pet = self
        self.care_tasks.append(task)

    def profile_summary(self) -> str:
        """Summarize the pet for display."""
        return f"{self.name} ({self.species}, {self.age_years} years old)"

    def add_care_note(self, note: str) -> None:
        """Store a short care note for this pet."""
        self.care_notes.append(note)

    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.care_tasks)


@dataclass
class Owner:
    name: str
    pets: List[Pet] = field(default_factory=list)
    preferences: List[str] = field(default_factory=list)
    daily_time_budget_minutes: int = 120

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def add_preference(self, preference: str) -> None:
        """Record an owner preference."""
        self.preferences.append(preference)

    def get_all_tasks(self) -> List[Task]:
        """Collect all tasks from every pet."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.care_tasks)
        return tasks

    def summary(self) -> str:
        """Return a short summary of the owner profile."""
        pet_count = len(self.pets)
        return f"{self.name} manages {pet_count} pet{'s' if pet_count != 1 else ''}."


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Create a scheduler for one owner."""
        self.owner = owner
        self._last_plan: List[Task] = []

    def collect_tasks(self) -> List[Task]:
        """Pull all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def _sort_key(self, task: Task) -> tuple[int, tuple[int, int], int, str]:
        return (
            PRIORITY_RANKS.get(task.priority.lower(), 3),
            _parse_time_label(task.preferred_time),
            task.duration_minutes,
            task.description.lower(),
        )

    def sort_tasks(self) -> List[Task]:
        """Order tasks by priority, time, and duration."""
        return sorted(self.collect_tasks(), key=self._sort_key)

    def build_plan(self) -> List[Task]:
        """Select the tasks that fit inside the owner's daily time budget."""
        remaining_minutes = self.owner.daily_time_budget_minutes
        plan: List[Task] = []

        for task in self.sort_tasks():
            if task.completed:
                task.skipped_reason = "already completed"
                continue

            if task.can_fit(remaining_minutes):
                task.skipped_reason = ""
                plan.append(task)
                remaining_minutes -= task.duration_minutes
            else:
                task.skipped_reason = "not enough time remaining"

        self._last_plan = plan
        return plan

    def explain_plan(self) -> str:
        """Explain the current schedule in readable text."""
        plan = self._last_plan or self.build_plan()
        if not plan:
            return "No tasks fit into today's schedule."

        lines = [f"Today's Schedule for {self.owner.name}:"]
        for task in plan:
            pet_label = f" for {task.pet.name}" if task.pet else ""
            lines.append(
                f"- {task.preferred_time or 'Anytime'}: {task.description}{pet_label} "
                f"({task.duration_minutes} min, priority: {task.priority})"
            )
        return "\n".join(lines)


SchedulePlanner = Scheduler