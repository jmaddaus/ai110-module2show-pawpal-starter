"""Automated tests for PawPal+ system."""

from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, timedelta


def test_task_completion():
    """Verify that calling mark_complete() changes the task's status."""
    task = Task("Morning walk", "07:30", 20, "high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_task_addition_increases_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    pet = Pet("Mochi", "dog", 3)
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task("Walk", "08:00", 20, "high"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task("Feed", "12:00", 10, "medium"))
    assert len(pet.get_tasks()) == 2
