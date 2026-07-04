# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- My initial UML design centers on four classes: `Owner`, `Pet`, `Task`, and `SchedulePlanner`.
- `Owner` stores the person's name, preferences, and pets so the app knows who the schedule is for.
- `Pet` stores each pet's profile and basic care details so the system can keep the plan tied to the right animal.
- `Task` represents one care action such as a walk, feeding, or grooming task, including its duration, priority, and category.
- `SchedulePlanner` takes the owner, pet, and task data and turns it into a daily plan by sorting and selecting tasks based on time and priority.
- The three core user actions I want to support are adding pet information, adding or editing care tasks, and generating a daily plan that explains what should happen first.

**b. Design changes**

- After reviewing the skeleton, I changed `Task` so it points to a `Pet` object instead of storing only a pet name string.
- I also changed `SchedulePlanner` to work from the `Owner` context alone, which lets it plan across all of the owner’s pets and use the owner’s time budget directly.
- Those changes reduce duplicated state and make the scheduling logic less likely to drift from the actual pet data.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- My scheduler considers preferred task time, priority, duration, pet ownership, and completion status.
- I treated exact time and priority as the most important because they are the clearest constraints for a pet owner trying to avoid missed care tasks.

**b. Tradeoffs**

- One tradeoff is that conflict detection only checks for exact matching start times, not overlapping durations.
- That is reasonable for this scenario because the app is still a lightweight planner, and exact-time collisions are the clearest conflicts to catch without adding much complexity.

---

## 3. AI Collaboration

**a. How you used AI**

- The most effective AI features were rapid code review, UML review, and targeted test planning.
- Prompts that worked best were narrow and concrete, such as asking how the scheduler should collect tasks from the owner or which edge cases mattered for a sorting and recurrence system.

**b. Judgment and verification**

- I rejected one early suggestion that would have made the scheduler plan across several disconnected time fields instead of keeping one readable preferred-time field.
- I verified the final approach by checking the demo output, reviewing the scheduler logic directly, and running the automated tests.

**c. Workflow and leadership**

- Separate chat sessions helped me keep design, implementation, testing, and documentation decisions isolated.
- That made it easier to compare ideas without mixing old assumptions into new phases.
- I learned that being the lead architect means deciding what to keep simple, rejecting elegant-looking complexity when it does not help the user, and using AI as a fast reviewer rather than an automatic decision-maker.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion, adding a task to a pet, recurring task creation, chronological sorting, filtering by pet and completion status, conflict detection, and the empty-owner edge case.
- These tests were important because they cover both the basic data model and the scheduler behavior that users actually rely on when planning pet care.

**b. Confidence**

- I am fairly confident in the current scheduler, around 4 out of 5 stars, because the main behaviors are covered by automated tests and the CLI demo output matches the expected plan.
- If I had more time, I would test overlapping time windows, multiple recurring tasks completing on the same day, and mixed priority ties to see how the scheduler behaves when the inputs are less clean.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with the way the scheduler stayed simple while still becoming useful: it sorts tasks, detects conflicts, handles recurrence, and still remains easy to read.

**b. What you would improve**

- In another iteration, I would add richer time handling, a clearer calendar-style UI, and a stronger recurrence model with explicit due dates instead of relying mostly on preferred time and completion flow.

**c. Key takeaway**

- I learned that the best way to work with AI is to treat it like a fast assistant, not the architect.
- When I kept the design boundaries clear and used separate chat sessions for each phase, it became much easier to make good decisions, verify them with tests, and keep the final system coherent.
