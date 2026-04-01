# PawPal+ Project Reflection

## 1. System Design
1. add a pet
2. schedule a walk 
3. see today's tasks

**a. Initial design**

- My system has four classes organized around a single chain of ownership:
Owner is the root. It holds a list of Pet objects and can aggregate all tasks across them.
Pet belongs to an Owner and carries its own list of Task objects — feeding, walking, meds, etc. are all attached to the specific animal they apply to.
Task is the core unit of work. It knows which Pet it belongs to, when it's due, how urgent it is, and whether it repeats.
Scheduler sits outside the ownership chain. It's stateless — it takes an Owner (and therefore all their pets and tasks) as input and handles the algorithmic work: sorting, conflict detection, and building the daily plan.
The key relationship is: Owner → Pet → Task, with Scheduler operating on that whole tree without being part of it.

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
