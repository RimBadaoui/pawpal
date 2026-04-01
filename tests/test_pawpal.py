import pytest
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


# Fixtures 

@pytest.fixture
def today():
    return datetime.today()

@pytest.fixture
def mochi():
    return Pet(name="Mochi", species="dog", breed="Shiba Inu", age=3)

@pytest.fixture
def luna():
    return Pet(name="Luna", species="cat", breed="Tabby", age=5)

@pytest.fixture
def owner(mochi, luna):
    o = Owner(name="Jordan", email="jordan@email.com")
    o.add_pet(mochi)
    o.add_pet(luna)
    return o


# Task tests 

def test_task_is_due_today(mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today, priority="high")
    assert task.is_due_today() is True

def test_task_not_due_today(mochi, today):
    tomorrow = today.replace(day=today.day + 1)
    task = Task(description="Walk", pet=mochi, due_time=tomorrow, priority="high")
    assert task.is_due_today() is False

def test_mark_complete(mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today, priority="high")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True

def test_next_occurrence_daily(mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today,
                priority="high", is_recurring=True, recurrence_rule="daily")
    from datetime import timedelta
    assert task.next_occurrence() == today + timedelta(days=1)

def test_next_occurrence_non_recurring(mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today, priority="high")
    assert task.next_occurrence() is None


# Pet tests 

def test_add_task(mochi, today):
    task = Task(description="Feed", pet=mochi, due_time=today, priority="medium")
    mochi.add_task(task)
    assert task in mochi.tasks

def test_get_upcoming_tasks_excludes_completed(mochi, today):
    task = Task(description="Feed", pet=mochi, due_time=today, priority="medium")
    mochi.add_task(task)
    task.mark_complete()
    assert task not in mochi.get_upcoming_tasks()


# Owner tests 

def test_add_pet(owner, mochi, luna):
    assert mochi in owner.pets
    assert luna in owner.pets

def test_get_all_tasks(owner, mochi, luna, today):
    t1 = Task(description="Walk",      pet=mochi, due_time=today, priority="high")
    t2 = Task(description="Breakfast", pet=luna,  due_time=today, priority="medium")
    mochi.add_task(t1)
    luna.add_task(t2)
    all_tasks = owner.get_all_tasks()
    assert t1 in all_tasks
    assert t2 in all_tasks

def test_get_todays_tasks(owner, mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today, priority="high")
    mochi.add_task(task)
    assert task in owner.get_todays_tasks()


# Scheduler tests 

def test_sorted_tasks_by_priority(owner, mochi, today):
    low  = Task(description="Playtime", pet=mochi, due_time=today.replace(hour=9),  priority="low")
    high = Task(description="Meds",     pet=mochi, due_time=today.replace(hour=10), priority="high")
    mochi.add_task(low)
    mochi.add_task(high)
    scheduler = Scheduler()
    sorted_tasks = scheduler.get_sorted_tasks(owner)
    assert sorted_tasks[0].priority == "high"

def test_detect_conflicts(owner, mochi, luna, today):
    same_time = today.replace(hour=9, minute=0, second=0, microsecond=0)
    t1 = Task(description="Walk",      pet=mochi, due_time=same_time, priority="high")
    t2 = Task(description="Vet visit", pet=luna,  due_time=same_time, priority="high")
    mochi.add_task(t1)
    luna.add_task(t2)
    scheduler = Scheduler()
    conflicts = scheduler.detect_conflicts(owner.get_todays_tasks())
    assert t1 in conflicts
    assert t2 in conflicts

def test_no_conflicts(owner, mochi, today):
    t1 = Task(description="Walk", pet=mochi, due_time=today.replace(hour=8), priority="high")
    t2 = Task(description="Feed", pet=mochi, due_time=today.replace(hour=9), priority="medium")
    mochi.add_task(t1)
    mochi.add_task(t2)
    scheduler = Scheduler()
    assert scheduler.detect_conflicts(owner.get_todays_tasks()) == []

def test_generate_daily_schedule(owner, mochi, today):
    task = Task(description="Walk", pet=mochi, due_time=today.replace(hour=8), priority="high")
    mochi.add_task(task)
    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(owner)
    assert task in schedule
