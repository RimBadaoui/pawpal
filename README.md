# PawPal+ 

**PawPal+**, a Streamlit app that helps pet owners plan care tasks for their pets.

Features
- Pet owners easily add/edit tasks and set deadlines for themselves
- PawPal+ generates a daily schedule based on task deadlines and priorities
- Keeps track of tasks and removes them once complete (walks, feeding, meds, enrichment, grooming, etc.)

## Testing Strategy

I wrote 17 tests across four areas of the system. For the core `Task` class, I verified that tasks correctly identify whether they're due today, that marking a task complete flips the flag, and that daily recurring tasks return the right next occurrence. For `Pet`, I checked that tasks are added properly and that completed tasks don't show up in the upcoming list. For `Owner`, I made sure pets and tasks are tracked correctly and that filtering to today's tasks works as expected.

The scheduler tests were the most important to me. I confirmed that tasks with the same priority sort in chronological order, that completing a daily recurring task automatically creates a new one for the following day, and that the conflict detector catches two tasks scheduled at the exact same time and reports both task names in the warning message.

Confidence Level: (4/5)

The core scheduling logic — sorting, conflict detection, and recurring task expansion — is well-covered and all tests pass. I'm holding back one star because weekly recurrence and month/year boundary rollovers aren't tested yet, and the duplicate-expansion guard in `_expand_recurring_tasks` still lacks direct test coverage. The system is solid for daily use but I'd want those gaps filled before calling it production-ready.
