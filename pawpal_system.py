"""PawPal+ System — Core logic layer for pet care scheduling."""

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    """Represents a single pet care activity."""
    description: str
    time: str  # HH:MM format
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    frequency: str = "once"  # "once", "daily", "weekly"
    completed: bool = False
    pet_name: str = ""
    date: str = ""  # YYYY-MM-DD format

    def mark_complete(self):
        """Mark this task as completed."""
        pass


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        pass

    def remove_task(self, description: str):
        """Remove a task by description."""
        pass

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        pass


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        pass

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        pass

    def remove_pet(self, name: str):
        """Remove a pet by name."""
        pass

    def get_pet(self, name: str):
        """Retrieve a pet by name."""
        pass

    def get_all_tasks(self) -> list:
        """Retrieve all tasks from all pets."""
        pass


class Scheduler:
    """The brain — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        pass

    def get_all_tasks(self) -> list:
        """Get all tasks from the owner's pets."""
        pass

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their scheduled time."""
        pass

    def filter_by_status(self, completed: bool = False) -> list:
        """Filter tasks by completion status."""
        pass

    def filter_by_pet(self, pet_name: str) -> list:
        """Filter tasks by pet name."""
        pass

    def detect_conflicts(self) -> list:
        """Detect tasks scheduled at the same time."""
        pass

    def mark_task_complete(self, task: Task):
        """Mark a task complete and handle recurrence."""
        pass

    def get_todays_schedule(self) -> list:
        """Return today's schedule sorted by time."""
        pass
