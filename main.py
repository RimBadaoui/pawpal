from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

# ── Setup ─────────────────────────────────────────────────────────────────────
owner = Owner(name="Jordan", email="jordan@email.com")

mochi = Pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)
luna  = Pet(name="Luna",  species="cat", breed="Tabby",    age=5)

owner.add_pet(mochi)
owner.add_pet(luna)

# ── Tasks (all due today at different times) ───────────────────────────────────
today = datetime.today()

mochi.add_task(Task(
    description="Morning walk",
    pet=mochi,
    due_time=today.replace(hour=8, minute=0, second=0, microsecond=0),
    priority="high",
    is_recurring=True,
    recurrence_rule="daily",
))

mochi.add_task(Task(
    description="Flea medication",
    pet=mochi,
    due_time=today.replace(hour=9, minute=30, second=0, microsecond=0),
    priority="high",
))

luna.add_task(Task(
    description="Breakfast",
    pet=luna,
    due_time=today.replace(hour=8, minute=30, second=0, microsecond=0),
    priority="medium",
    is_recurring=True,
    recurrence_rule="daily",
))

luna.add_task(Task(
    description="Playtime",
    pet=luna,
    due_time=today.replace(hour=17, minute=0, second=0, microsecond=0),
    priority="low",
))

# ── Generate & print schedule ─────────────────────────────────────────────────
scheduler = Scheduler()
schedule = scheduler.generate_daily_schedule(owner)
conflicts = scheduler.detect_conflicts(schedule)

print("=" * 45)
print(f"  PawPal+ — Today's Schedule for {owner.name}")
print("=" * 45)

if not schedule:
    print("  No tasks scheduled for today.")
else:
    for task in schedule:
        time_str     = task.due_time.strftime("%I:%M %p")
        recurring    = " (recurring)" if task.is_recurring else ""
        conflict_flag = " CONFLICT" if task in conflicts else ""
        print(f"  [{task.priority.upper():6}]  {time_str}  |  {task.pet.name}: {task.description}{recurring}{conflict_flag}")

print("=" * 45)
print(f"  Total tasks: {len(schedule)}")
print("=" * 45)
