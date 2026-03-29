"""Automated tests for PawPal+ system."""

from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date, timedelta


# --- Basic Tests (Phase 2) ---

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


# --- Sorting Tests (Phase 5) ---

def test_sort_by_time():
    """Verify tasks are returned in chronological order after sorting."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    pet.add_task(Task("Evening walk", "17:00", 30, "high"))
    pet.add_task(Task("Morning walk", "07:30", 20, "high"))
    pet.add_task(Task("Lunch feeding", "12:00", 10, "medium"))

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()

    assert sorted_tasks[0].time == "07:30"
    assert sorted_tasks[1].time == "12:00"
    assert sorted_tasks[2].time == "17:00"


# --- Recurrence Tests (Phase 5) ---

def test_daily_recurrence():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    today = str(date.today())
    tomorrow = str(date.today() + timedelta(days=1))

    pet.add_task(Task("Morning walk", "07:30", 20, "high", frequency="daily", date=today))

    scheduler = Scheduler(owner)
    original_task = pet.get_tasks()[0]
    scheduler.mark_task_complete(original_task)

    assert original_task.completed is True
    assert len(pet.get_tasks()) == 2

    new_task = pet.get_tasks()[1]
    assert new_task.date == tomorrow
    assert new_task.completed is False
    assert new_task.frequency == "daily"


def test_weekly_recurrence():
    """Confirm that marking a weekly task complete creates a new task 7 days later."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    today = str(date.today())
    next_week = str(date.today() + timedelta(weeks=1))

    pet.add_task(Task("Flea medication", "09:00", 5, "medium", frequency="weekly", date=today))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet.get_tasks()[0])

    assert len(pet.get_tasks()) == 2
    assert pet.get_tasks()[1].date == next_week


# --- Conflict Detection Tests (Phase 5) ---

def test_detect_conflicts():
    """Verify that the Scheduler flags tasks at the same time on the same day."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    today = str(date.today())
    pet.add_task(Task("Morning walk", "07:30", 20, "high", date=today))
    pet.add_task(Task("Breakfast", "07:30", 10, "high", date=today))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 1
    assert "07:30" in conflicts[0]


def test_no_conflicts_different_times():
    """Verify no conflicts when tasks are at different times."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    today = str(date.today())
    pet.add_task(Task("Walk", "07:30", 20, "high", date=today))
    pet.add_task(Task("Feed", "12:00", 10, "medium", date=today))

    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()

    assert len(conflicts) == 0


# --- Edge Case Tests (Phase 5) ---

def test_pet_with_no_tasks():
    """Verify scheduler handles a pet with no tasks gracefully."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_owner_with_no_pets():
    """Verify scheduler handles an owner with no pets gracefully."""
    owner = Owner("Test")
    scheduler = Scheduler(owner)

    assert scheduler.get_all_tasks() == []
    assert scheduler.get_todays_schedule() == []
    assert scheduler.detect_conflicts() == []


def test_filter_by_pet():
    """Verify filtering tasks by pet name returns correct subset."""
    owner = Owner("Test")
    dog = Pet("Buddy", "dog", 2)
    cat = Pet("Whiskers", "cat", 4)
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk", "08:00", 20, "high"))
    cat.add_task(Task("Feed", "08:00", 10, "high"))

    scheduler = Scheduler(owner)
    buddy_tasks = scheduler.filter_by_pet("Buddy")

    assert len(buddy_tasks) == 1
    assert buddy_tasks[0].description == "Walk"


def test_filter_by_status():
    """Verify filtering by completion status works correctly."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    task1 = Task("Walk", "08:00", 20, "high")
    task2 = Task("Feed", "12:00", 10, "medium")
    pet.add_task(task1)
    pet.add_task(task2)
    task1.mark_complete()

    scheduler = Scheduler(owner)
    pending = scheduler.filter_by_status(completed=False)
    done = scheduler.filter_by_status(completed=True)

    assert len(pending) == 1
    assert len(done) == 1
    assert pending[0].description == "Feed"
    assert done[0].description == "Walk"


def test_once_task_no_recurrence():
    """Verify that a one-time task does not create a recurring instance."""
    owner = Owner("Test")
    pet = Pet("Buddy", "dog", 2)
    owner.add_pet(pet)

    pet.add_task(Task("Vet visit", "14:00", 60, "high", frequency="once"))

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete(pet.get_tasks()[0])

    assert len(pet.get_tasks()) == 1
