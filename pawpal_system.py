from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    description: str
    pet: Pet
    due_time: datetime
    priority: str                      # "low", "medium", "high"
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None   # e.g. "daily", "weekly", or None

    def mark_complete(self):
        pass

    def is_due_today(self) -> bool:
        pass

    def next_occurrence(self) -> Optional[datetime]:
        pass


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def get_upcoming_tasks(self) -> list[Task]:
        pass


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        pass

    def get_all_tasks(self) -> list[Task]:
        pass

    def get_todays_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def get_sorted_tasks(self, owner: Owner) -> list[Task]:
        pass

    def detect_conflicts(self, tasks: list[Task]) -> list[Task]:
        pass

    def generate_daily_schedule(self, owner: Owner) -> list[Task]:
        pass
