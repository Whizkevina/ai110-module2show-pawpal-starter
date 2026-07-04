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
