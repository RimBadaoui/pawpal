# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## Testing PawPal+

To run the test suite:

```bash
python -m pytest
```

I wrote 17 tests across four areas of the system. For the core `Task` class, I verified that tasks correctly identify whether they're due today, that marking a task complete flips the flag, and that daily recurring tasks return the right next occurrence. For `Pet`, I checked that tasks are added properly and that completed tasks don't show up in the upcoming list. For `Owner`, I made sure pets and tasks are tracked correctly and that filtering to today's tasks works as expected.

The scheduler tests were the most important to me. I confirmed that tasks with the same priority sort in chronological order, that completing a daily recurring task automatically creates a new one for the following day, and that the conflict detector catches two tasks scheduled at the exact same time and reports both task names in the warning message.

**Confidence Level: ⭐⭐⭐⭐ (4/5)**

The core scheduling logic — sorting, conflict detection, and recurring task expansion — is well-covered and all tests pass. I'm holding back one star because weekly recurrence and month/year boundary rollovers aren't tested yet, and the duplicate-expansion guard in `_expand_recurring_tasks` still lacks direct test coverage. The system is solid for daily use but I'd want those gaps filled before calling it production-ready.
