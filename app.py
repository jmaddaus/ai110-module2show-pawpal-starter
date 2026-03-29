import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler
from datetime import date

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("A smart pet care management system that helps owners keep their furry friends happy and healthy.")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

owner = st.session_state.owner

# --- Sidebar: Owner & Pet Management ---
with st.sidebar:
    st.header("Owner & Pets")
    owner.name = st.text_input("Owner name", value=owner.name)

    st.subheader("Add a Pet")
    with st.form("add_pet_form", clear_on_submit=True):
        pet_name = st.text_input("Pet name")
        species = st.selectbox("Species", ["dog", "cat", "bird", "fish", "other"])
        age = st.number_input("Age", min_value=0, max_value=30, value=1)
        add_pet = st.form_submit_button("Add Pet")
        if add_pet and pet_name:
            if owner.get_pet(pet_name) is None:
                owner.add_pet(Pet(name=pet_name, species=species, age=age))
                st.success(f"Added {pet_name}!")
            else:
                st.warning(f"A pet named '{pet_name}' already exists.")

    if owner.pets:
        st.subheader("Your Pets")
        for pet in owner.pets:
            st.write(f"**{pet.name}** ({pet.species}, age {pet.age}) — {len(pet.tasks)} tasks")

# --- Main Area: Task Management ---
st.subheader("Schedule a Task")

if not owner.pets:
    st.info("Add a pet in the sidebar first.")
else:
    with st.form("add_task_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            task_desc = st.text_input("Task description", value="Morning walk")
            task_time = st.text_input("Time (HH:MM)", value="08:00")
            task_pet = st.selectbox("Pet", [p.name for p in owner.pets])
        with col2:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
            frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])

        add_task = st.form_submit_button("Add Task")
        if add_task and task_desc and task_time:
            pet = owner.get_pet(task_pet)
            if pet:
                new_task = Task(
                    description=task_desc,
                    time=task_time,
                    duration_minutes=int(duration),
                    priority=priority,
                    frequency=frequency,
                    date=str(date.today()),
                )
                pet.add_task(new_task)
                st.success(f"Added '{task_desc}' for {task_pet} at {task_time}!")

    # --- Schedule Display ---
    st.divider()
    st.subheader("Today's Schedule")

    scheduler = Scheduler(owner)
    schedule = scheduler.get_todays_schedule()

    # Show conflict warnings
    conflicts = scheduler.detect_conflicts()
    if conflicts:
        for warning in conflicts:
            st.warning(f"⚠️ {warning}")

    if schedule:
        # Build table data
        table_data = []
        for task in schedule:
            table_data.append({
                "Time": task.time,
                "Task": task.description,
                "Pet": task.pet_name,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority.capitalize(),
                "Frequency": task.frequency.capitalize(),
            })
        st.table(table_data)

        # Mark tasks complete
        st.subheader("Mark Complete")
        for i, task in enumerate(schedule):
            if st.button(f"✅ {task.description} ({task.pet_name})", key=f"complete_{i}"):
                scheduler.mark_task_complete(task)
                st.success(f"Marked '{task.description}' complete!")
                if task.frequency in ("daily", "weekly"):
                    st.info(f"Recurring task — next occurrence auto-scheduled.")
                st.rerun()
    else:
        st.info("No tasks scheduled for today. Add some above!")

    # --- Filtered Views ---
    if owner.pets and scheduler.get_all_tasks():
        st.divider()
        st.subheader("Filter Tasks")
        col1, col2 = st.columns(2)
        with col1:
            filter_pet = st.selectbox("Filter by pet", ["All"] + [p.name for p in owner.pets])
        with col2:
            filter_status = st.selectbox("Filter by status", ["Pending", "Completed", "All"])

        if filter_pet != "All":
            filtered = scheduler.filter_by_pet(filter_pet)
        else:
            filtered = scheduler.get_all_tasks()

        if filter_status == "Pending":
            filtered = [t for t in filtered if not t.completed]
        elif filter_status == "Completed":
            filtered = [t for t in filtered if t.completed]

        if filtered:
            filter_data = []
            for task in scheduler.sort_by_time(filtered):
                status = "✅ Done" if task.completed else "⏳ Pending"
                filter_data.append({
                    "Time": task.time,
                    "Task": task.description,
                    "Pet": task.pet_name,
                    "Priority": task.priority.capitalize(),
                    "Status": status,
                    "Date": task.date,
                })
            st.table(filter_data)
        else:
            st.info("No tasks match the current filter.")
