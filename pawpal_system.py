from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


@dataclass
class Task:
    description: str
    pet: Pet
    due_time: datetime
    priority: str                        # "low", "medium", "high"
    is_recurring: bool = False
    recurrence_rule: Optional[str] = None  # "daily" | "weekly" | None
    completed: bool = False

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True

    def is_due_today(self) -> bool:
        """Return True if the task's due date is today."""
        return self.due_time.date() == datetime.today().date()

    def next_occurrence(self) -> Optional[datetime]:
        """Return the next due datetime for a recurring task, or None if not recurring."""
        if not self.is_recurring or self.recurrence_rule is None:
            return None
        if self.recurrence_rule == "daily":
            return self.due_time + timedelta(days=1)
        if self.recurrence_rule == "weekly":
            return self.due_time + timedelta(weeks=1)
        return None


@dataclass
class Pet:
    name: str
    species: str
    breed: str
    age: int
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def get_upcoming_tasks(self) -> list[Task]:
        """Return all incomplete tasks scheduled from now onward."""
        now = datetime.now()
        return [t for t in self.tasks if t.due_time >= now and not t.completed]


class Owner:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]

    def get_todays_tasks(self) -> list[Task]:
        """Return all tasks due today across every pet."""
        return [t for t in self.get_all_tasks() if t.is_due_today()]


class Scheduler:
    def get_sorted_tasks(self, owner: Owner) -> list[Task]:
        """Sort today's incomplete tasks by priority then due time."""
        tasks = [t for t in owner.get_todays_tasks() if not t.completed]
        return sorted(tasks, key=lambda t: (PRIORITY_ORDER[t.priority], t.due_time))

    def detect_conflicts(self, tasks: list[Task]) -> list[Task]:
        """Return tasks that share the exact same due_time (scheduling conflict)."""
        conflicts = []
        for i, task_a in enumerate(tasks):
            for task_b in tasks[i + 1:]:
                if task_a.due_time == task_b.due_time and task_a not in conflicts:
                    conflicts.append(task_a)
                    conflicts.append(task_b)
        return conflicts

    def generate_daily_schedule(self, owner: Owner) -> list[Task]:
        """Return today's sorted, incomplete tasks with recurring tasks expanded."""
        self._expand_recurring_tasks(owner)
        return self.get_sorted_tasks(owner)

    def _expand_recurring_tasks(self, owner: Owner):
        """For each recurring task not yet scheduled today, create today's instance."""
        today = datetime.today().date()
        for pet in owner.pets:
            new_tasks = []
            for task in pet.tasks:
                if not task.is_recurring:
                    continue
                already_today = any(
                    t.description == task.description and t.due_time.date() == today
                    for t in pet.tasks
                )
                if not already_today:
                    next_time = task.next_occurrence()
                    if next_time and next_time.date() == today:
                        new_tasks.append(Task(
                            description=task.description,
                            pet=pet,
                            due_time=next_time,
                            priority=task.priority,
                            is_recurring=task.is_recurring,
                            recurrence_rule=task.recurrence_rule,
                        ))
            for t in new_tasks:
                pet.add_task(t)
