# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

Three core actions a user should be able to perform:
1. **Add a pet** — Register a new pet with basic info (name, species, age) so the system knows who to schedule care for.
2. **Schedule a task** — Create care tasks (walks, feedings, medications) with a time, duration, priority, and optional recurrence for a specific pet.
3. **View today's schedule** — See a sorted, conflict-checked daily plan showing all tasks across all pets.

I designed four classes to support these actions:
- **Task** (dataclass): Represents a single care activity. Holds description, scheduled time, duration, priority level, frequency (once/daily/weekly), completion status, associated pet name, and date. Responsible for marking itself complete.
- **Pet** (dataclass): Stores pet details (name, species, age) and maintains a list of tasks. Responsible for adding, removing, and retrieving its own tasks.
- **Owner**: Represents the pet owner. Manages a list of pets and provides access to all tasks across all pets. Acts as the central data holder.
- **Scheduler**: The "brain" of the system. Takes an Owner reference and provides algorithmic logic — sorting tasks by time, filtering by status or pet, detecting scheduling conflicts, handling recurring task generation, and producing a daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
