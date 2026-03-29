"""PawPal+ CLI Demo — Verifies backend logic in the terminal."""

from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date


def main():
    # Create an owner
    owner = Owner("Jordan")
    print(f"Owner: {owner.name}\n")

    # Create two pets
    mochi = Pet(name="Mochi", species="dog", age=3)
    whiskers = Pet(name="Whiskers", species="cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(whiskers)

    # Add tasks (out of order to test sorting)
    today = str(date.today())

    mochi.add_task(Task("Evening walk", "17:00", 30, "high", "daily", date=today))
    mochi.add_task(Task("Morning walk", "07:30", 20, "high", "daily", date=today))
    mochi.add_task(Task("Flea medication", "09:00", 5, "medium", "weekly", date=today))

    whiskers.add_task(Task("Breakfast feeding", "07:30", 10, "high", "daily", date=today))
    whiskers.add_task(Task("Litter box cleaning", "12:00", 10, "medium", "daily", date=today))
    whiskers.add_task(Task("Vet appointment", "14:00", 60, "high", "once", date=today))

    # Create scheduler
    scheduler = Scheduler(owner)

    # Print today's schedule (sorted by time)
    print("=" * 55)
    print(f"  Today's Schedule — {today}")
    print("=" * 55)
    schedule = scheduler.get_todays_schedule()
    for task in schedule:
        status = "Done" if task.completed else "Pending"
        print(f"  {task.time}  [{task.priority.upper():^6}]  {task.description:<25} ({task.pet_name}) - {status}")
    print()

    # Check for conflicts
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        print("Scheduling Conflicts:")
        for warning in conflicts:
            print(f"  WARNING: {warning}")
        print()

    # Filter by pet
    print(f"Tasks for Mochi:")
    for task in scheduler.filter_by_pet("Mochi"):
        print(f"  {task.time}  {task.description}")
    print()

    # Mark a task complete and show recurrence
    print("Marking 'Morning walk' as complete...")
    morning_walk = schedule[0]  # First task after sorting (07:30)
    scheduler.mark_task_complete(morning_walk)
    print(f"  '{morning_walk.description}' completed: {morning_walk.completed}")

    # Show that a new recurring task was created
    mochi_tasks = mochi.get_tasks()
    print(f"  Mochi now has {len(mochi_tasks)} tasks (new recurring task added)")
    for task in mochi_tasks:
        print(f"    {task.date} {task.time} - {task.description} (completed: {task.completed})")
    print()

    # Filter by status
    pending = scheduler.filter_by_status(completed=False)
    print(f"Pending tasks remaining: {len(pending)}")


if __name__ == "__main__":
    main()
