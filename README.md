# PawPal+ (Module 2 Project)

**PawPal+** is a smart pet care management system built with Python and Streamlit. It helps pet owners plan daily care tasks — walks, feedings, medications, and appointments — while using algorithmic logic to organize and prioritize schedules.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

## Features

- **Owner & Pet Management**: Register multiple pets with name, species, and age. Manage them from the sidebar.
- **Task Scheduling**: Add tasks with description, time, duration, priority (low/medium/high), and frequency (once/daily/weekly).
- **Daily Schedule View**: See all of today's tasks sorted chronologically in a clean table.
- **Mark Complete**: Check off tasks as done directly from the UI.
- **Conflict Warnings**: Automatic alerts when two tasks overlap at the same time.
- **Recurring Tasks**: Daily and weekly tasks auto-regenerate for the next occurrence when completed.
- **Filter & Search**: Filter tasks by pet name or completion status.

## Smarter Scheduling

PawPal+ includes several algorithmic features that make scheduling intelligent:

- **Sort by time**: Tasks are automatically sorted in chronological order using Python's `sorted()` with a lambda key on HH:MM time strings, so the daily schedule always reads top-to-bottom.
- **Filter by pet or status**: View tasks for a specific pet or see only pending/completed tasks to focus on what matters.
- **Conflict detection**: The scheduler scans all tasks and warns when two or more are scheduled at the exact same time on the same day, helping owners avoid double-booking.
- **Recurring tasks**: Daily and weekly tasks automatically generate a new occurrence for the next date when marked complete, using Python's `timedelta` for accurate date arithmetic.

## System Architecture

The system is built with four core classes (see `uml_final.md` for the full Mermaid.js diagram):

- **Task** (dataclass): A single care activity with time, priority, frequency, and completion tracking.
- **Pet** (dataclass): Holds pet info and manages its own task list.
- **Owner**: Manages multiple pets and aggregates all tasks.
- **Scheduler**: The brain — sorts, filters, detects conflicts, handles recurrence, and produces daily schedules.

## Testing PawPal+

Run the test suite with:

```bash
python -m pytest -v
```

The test suite covers 12 tests across these areas:

- **Task completion**: Verifies `mark_complete()` changes task status
- **Task addition**: Confirms adding tasks increases a pet's task count
- **Sorting correctness**: Tasks are returned in chronological order by time
- **Daily recurrence**: Completing a daily task creates a new one for the next day
- **Weekly recurrence**: Completing a weekly task creates a new one 7 days later
- **One-time tasks**: Non-recurring tasks do not generate new instances
- **Conflict detection**: Same-time tasks are flagged; different-time tasks are not
- **Filtering**: Tasks can be filtered by pet name and by completion status
- **Edge cases**: Empty pets and empty owners are handled gracefully

**Confidence Level**: ⭐⭐⭐⭐ (4/5) — All happy paths and key edge cases are covered. Additional testing for overlapping time windows and multi-day scheduling would increase confidence further.

## Getting Started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the App

```bash
streamlit run app.py
```

### Run the CLI Demo

```bash
python main.py
```

### Run Tests

```bash
python -m pytest -v
```
