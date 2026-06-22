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
