import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

# ── Session state init ─────────────────────────────────────────────────────────
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="", email="")

# ── Owner setup ────────────────────────────────────────────────────────────────
st.subheader("Owner")
owner_name = st.text_input("Your name", value="Jordan")
st.session_state.owner.name = owner_name

# ── Add a pet ──────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Pet")

col1, col2, col3, col4 = st.columns(4)
with col1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col2:
    species = st.selectbox("Species", ["dog", "cat", "other"])
with col3:
    breed = st.text_input("Breed", value="Shiba Inu")
with col4:
    age = st.number_input("Age", min_value=0, max_value=30, value=3)

if st.button("Add pet"):
    new_pet = Pet(name=pet_name, species=species, breed=breed, age=age)
    st.session_state.owner.add_pet(new_pet)
    st.success(f"{pet_name} added!")

if st.session_state.owner.pets:
    st.write("**Your pets:**")
    st.table([
        {"Name": p.name, "Species": p.species, "Breed": p.breed, "Age": p.age}
        for p in st.session_state.owner.pets
    ])
else:
    st.info("No pets yet. Add one above.")

# ── Add a task ─────────────────────────────────────────────────────────────────
st.divider()
st.subheader("Add a Task")

if not st.session_state.owner.pets:
    st.warning("Add a pet first before scheduling tasks.")
else:
    pet_names = [p.name for p in st.session_state.owner.pets]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        selected_pet_name = st.selectbox("Pet", pet_names)
    with col2:
        task_title = st.text_input("Task", value="Morning walk")
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        due_hour = st.number_input("Hour (24h)", min_value=0, max_value=23, value=8)

    is_recurring = st.checkbox("Recurring?")
    recurrence_rule = None
    if is_recurring:
        recurrence_rule = st.selectbox("Repeat", ["daily", "weekly"])

    if st.button("Add task"):
        selected_pet = next(p for p in st.session_state.owner.pets if p.name == selected_pet_name)
        due_time = datetime.today().replace(hour=due_hour, minute=0, second=0, microsecond=0)
        new_task = Task(
            description=task_title,
            pet=selected_pet,
            due_time=due_time,
            priority=priority,
            is_recurring=is_recurring,
            recurrence_rule=recurrence_rule,
        )
        selected_pet.add_task(new_task)
        st.success(f"Task '{task_title}' added for {selected_pet_name}!")
        conflicts = Scheduler().detect_conflicts(st.session_state.owner.get_all_tasks())
        for message in conflicts:
            st.warning(f"Scheduling conflict: {message}")

    all_tasks = st.session_state.owner.get_all_tasks()
    if all_tasks:
        st.write("**All tasks:**")
        st.table([
            {
                "Pet": t.pet.name,
                "Task": t.description,
                "Priority": t.priority,
                "Due": t.due_time.strftime("%I:%M %p"),
                "Recurring": t.recurrence_rule or "no",
            }
            for t in all_tasks
        ])

# ── Generate schedule ──────────────────────────────────────────────────────────
st.divider()
st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler()
    schedule = scheduler.generate_daily_schedule(st.session_state.owner)
    conflicts = scheduler.detect_conflicts(schedule)

    if not schedule:
        st.info("No tasks scheduled for today.")
    else:
        for task in schedule:
            conflict_flag = " — CONFLICT" if task in conflicts else ""
            recurring_flag = " (recurring)" if task.is_recurring else ""
            st.markdown(
                f"**[{task.priority.upper()}]** {task.due_time.strftime('%I:%M %p')} "
                f"— {task.pet.name}: {task.description}{recurring_flag}{conflict_flag}"
            )
