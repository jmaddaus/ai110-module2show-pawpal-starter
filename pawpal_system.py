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

    def __post_init__(self):
        """Set default date to today if not provided."""
        if not self.date:
            self.date = str(date.today())

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    """Stores pet details and a list of tasks."""
    name: str
    species: str
    age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str):
        """Remove a task by description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_tasks(self) -> list:
        """Return all tasks for this pet."""
        return self.tasks


class Owner:
    """Manages multiple pets and provides access to all their tasks."""

    def __init__(self, name: str):
        """Initialize owner with a name and empty pets list."""
        self.name = name
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet):
        """Add a pet to this owner."""
        self.pets.append(pet)

    def remove_pet(self, name: str):
        """Remove a pet by name."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_pet(self, name: str):
        """Retrieve a pet by name. Returns None if not found."""
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def get_all_tasks(self) -> list:
        """Retrieve all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    """The brain — retrieves, organizes, and manages tasks across pets."""

    def __init__(self, owner: Owner):
        """Initialize scheduler with an owner reference."""
        self.owner = owner

    def get_all_tasks(self) -> list:
        """Get all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list = None) -> list:
        """Sort tasks by their scheduled time (HH:MM)."""
        if tasks is None:
            tasks = self.get_all_tasks()
        return sorted(tasks, key=lambda t: t.time)

    def filter_by_status(self, completed: bool = False) -> list:
        """Filter tasks by completion status."""
        return [t for t in self.get_all_tasks() if t.completed == completed]

    def filter_by_pet(self, pet_name: str) -> list:
        """Filter tasks by pet name."""
        return [t for t in self.get_all_tasks() if t.pet_name == pet_name]

    def detect_conflicts(self) -> list:
        """Detect tasks scheduled at the same time and return warning messages."""
        tasks = self.get_all_tasks()
        conflicts = []
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if tasks[i].time == tasks[j].time and tasks[i].date == tasks[j].date:
                    conflicts.append(
                        f"Conflict: '{tasks[i].description}' ({tasks[i].pet_name}) "
                        f"and '{tasks[j].description}' ({tasks[j].pet_name}) "
                        f"are both scheduled at {tasks[i].time} on {tasks[i].date}"
                    )
        return conflicts

    def mark_task_complete(self, task: Task):
        """Mark a task complete and auto-create next occurrence for recurring tasks."""
        task.mark_complete()

        if task.frequency in ("daily", "weekly"):
            current_date = date.fromisoformat(task.date)
            if task.frequency == "daily":
                next_date = current_date + timedelta(days=1)
            else:
                next_date = current_date + timedelta(weeks=1)

            new_task = Task(
                description=task.description,
                time=task.time,
                duration_minutes=task.duration_minutes,
                priority=task.priority,
                frequency=task.frequency,
                completed=False,
                pet_name=task.pet_name,
                date=str(next_date),
            )

            pet = self.owner.get_pet(task.pet_name)
            if pet:
                pet.add_task(new_task)

    def get_todays_schedule(self) -> list:
        """Return today's incomplete tasks sorted by time."""
        today = str(date.today())
        tasks = [t for t in self.get_all_tasks() if t.date == today and not t.completed]
        return self.sort_by_time(tasks)
