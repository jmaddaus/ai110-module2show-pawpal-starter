<!-- @format -->

# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:

1. **Add a pet** - Register a new pet with basic info (name, species, age) so the system knows who to schedule care for.
2. **Schedule a task** - Create care tasks (walks, feedings, medications) with a time, duration, priority, and optional recurrence for a specific pet.
3. **View today's schedule** - See a sorted, conflict-checked daily plan showing all tasks across all pets.

I designed four classes to support these actions:

- **Task** (dataclass): Represents a single care activity. Holds description, scheduled time, duration, priority level, frequency (once/daily/weekly), completion status, associated pet name, and date. Responsible for marking itself complete.
- **Pet** (dataclass): Stores pet details (name, species, age) and maintains a list of tasks. Responsible for adding, removing, and retrieving its own tasks.
- **Owner**: Represents the pet owner. Manages a list of pets and provides access to all tasks across all pets. Acts as the central data holder.
- **Scheduler**: The "brain" of the system. Takes an Owner reference and provides algorithmic logic sorting tasks by time, filtering by status or pet, detecting scheduling conflicts, handling recurring task generation, and producing a daily schedule.

**b. Design changes**

Yes, the design changed during implementation. The most significant change was adding a `date` field to the Task class. In the initial UML sketch, tasks only had a `time` (HH:MM) field. During implementation, I realized that recurring tasks need a date to determine when the next occurrence should be scheduled, and `get_todays_schedule()` needs to filter by date. I also added `__post_init__` to Task so that the date defaults to today if not provided, which keeps the API simple for one-off tasks while supporting multi-day scheduling for recurrence.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers three main constraints:

- **Time**: Tasks are sorted by their HH:MM start time so the daily schedule reads chronologically. This is the primary organizing principle.
- **Priority**: Each task has a priority level (low, medium, high) displayed prominently in the UI so owners can see at a glance what matters most.
- **Frequency**: Tasks can be one-time, daily, or weekly. The scheduler automatically handles recurrence when tasks are completed, so owners don't have to manually re-enter routine care activities.

I decided time was the most important constraint because a daily schedule only makes sense if it's ordered chronologically as that's how a pet owner actually moves through their day. Priority is secondary information that helps the owner decide what to tackle first if they're short on time.

**b. Tradeoffs**

One key tradeoff the scheduler makes is that conflict detection only checks for **exact time matches** rather than detecting overlapping durations. For example, if a 30-minute walk starts at 07:30 and a 10-minute feeding also starts at 07:30, the scheduler flags a conflict. However, if the walk is at 07:30 (30 min) and feeding is at 07:45, the scheduler does not flag them even though they overlap in practice.

This tradeoff is reasonable for a pet care scenario because most pet owners think in terms of "what time does this start?" rather than calculating overlapping time windows. The simplicity makes the conflict warnings easy to understand and act on. A duration-aware overlap algorithm would add complexity that isn't necessary for typical pet care scheduling where tasks are generally spaced out through the day.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI (Claude Code) throughout this project in several ways:

- **Design brainstorming**: I described the pet care scenario and asked for help drafting a Mermaid.js UML class diagram showing the four main classes and their relationships. This gave me a visual blueprint before writing any code.
- **Scaffolding**: I used AI to generate the initial class skeletons with proper dataclass decorators and type hints, then fleshed out the logic incrementally.
- **Implementation**: For algorithmic features like recurring task generation with `timedelta` and conflict detection, I described what I wanted and reviewed the generated code to make sure it handled edge cases.
- **Testing**: I asked AI to generate pytest tests covering happy paths and edge cases, then reviewed each test to ensure it was testing meaningful behavior.

The most helpful prompts were specific and scoped like "implement a method that detects tasks at the same time and returns warning strings" rather than vague requests. Providing context about what already existed (the Owner/Pet/Task structure) helped get accurate suggestions.

**b. Judgment and verification**

When generating the Streamlit UI, the AI initially suggested a more complex session state management approach using multiple separate keys for owner, pets, and tasks individually. I simplified this to store just the single Owner object in `st.session_state`, since the Owner already holds references to all pets and their tasks. Keeping one root object in session state was cleaner and avoided synchronization issues between separate state entries.

I verified this by running the Streamlit app and confirming that adding pets and tasks persisted correctly across page reruns, and that the schedule displayed the right data after multiple interactions.

---

## 4. Testing and Verification

**a. What you tested**

I tested 12 behaviors across five categories:

- **Core functionality**: Task completion status changes, task count increases when adding tasks to a pet.
- **Sorting**: Tasks come back in chronological order regardless of insertion order.
- **Recurrence**: Daily tasks generate a next-day occurrence, weekly tasks generate a next-week occurrence, and one-time tasks do not recur.
- **Conflict detection**: Same-time tasks produce warnings, different-time tasks do not.
- **Edge cases**: Empty pet (no tasks) and empty owner (no pets) don't crash the scheduler.

These tests were important because they verify the core algorithmic "brain" of the system. If sorting is wrong, the schedule is useless. If recurrence is broken, daily routines fall apart. If conflict detection has false positives/negatives, owners lose trust in the warnings.

**b. Confidence**

I'm fairly confident the scheduler works correctly for its intended use case — **4 out of 5 stars**. All happy paths and important edge cases pass.

If I had more time, I would test:

- **Overlapping time windows** (duration-aware conflicts)
- **Tasks spanning midnight** (e.g., a late-night task that runs past 00:00)
- **Large datasets** (performance with 100+ tasks across many pets)
- **Date boundary edge cases** (tasks created on Feb 28 with daily recurrence)

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the "CLI-first" workflow. Building and verifying all the logic in `main.py` before touching the Streamlit UI meant that by the time I wired up the frontend, the backend was already solid. The demo script served as both a verification tool and a quick reference for how the classes interact. This approach prevented the common trap of debugging logic issues through a UI layer.

**b. What you would improve**

If I had another iteration, I would redesign conflict detection to be duration-aware: checking whether tasks actually overlap in their time windows rather than just matching start times. I would also add data persistence (saving to JSON) so that pets and tasks survive between app restarts, and add the ability to edit or reschedule existing tasks rather than only adding new ones.

**c. Key takeaway**

The most important thing I learned is that AI works best as an accelerator when you already have a clear design in mind. Starting with the UML diagram meant I could give AI specific, well-scoped instructions rather than vague "build me an app" requests. The human role as architect is what keeps the system coherent. AI excels at generating boilerplate and suggesting implementations, but the design judgment has to come from the developer.
