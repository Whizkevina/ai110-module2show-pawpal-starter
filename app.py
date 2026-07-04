import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")

owner = st.session_state.owner

st.subheader("Owner and Pets")
owner_name = st.text_input("Owner name", value=owner.name)
if owner_name != owner.name:
    owner.name = owner_name

with st.form("add_pet_form", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age_years = st.number_input("Age (years)", min_value=0, max_value=30, value=0)
    add_pet = st.form_submit_button("Add pet")

    if add_pet and pet_name.strip():
        owner.add_pet(Pet(name=pet_name.strip(), species=species, age_years=int(age_years)))

if owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {
                "name": pet.name,
                "species": pet.species,
                "age_years": pet.age_years,
                "tasks": pet.task_count(),
            }
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one below.")

st.markdown("### Tasks")
st.caption("Add care tasks directly to a pet so they persist in session state.")

if owner.pets:
    with st.form("add_task_form", clear_on_submit=True):
        task_description = st.text_input("Task description", value="Morning walk")
        col1, col2, col3 = st.columns(3)
        with col1:
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        with col3:
            preferred_time = st.text_input("Preferred time", value="08:00")

        pet_options = [f"{pet.name} ({pet.species})" for pet in owner.pets]
        selected_pet_label = st.selectbox("Assign to pet", pet_options)
        add_task = st.form_submit_button("Add task")

        if add_task and task_description.strip():
            selected_pet = owner.pets[pet_options.index(selected_pet_label)]
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(duration),
                    priority=priority,
                    preferred_time=preferred_time.strip(),
                )
            )

    all_tasks = owner.get_all_tasks()
    if all_tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "description": task.description,
                    "pet": task.pet.name if task.pet else "",
                    "duration_minutes": task.duration_minutes,
                    "priority": task.priority,
                    "preferred_time": task.preferred_time,
                }
                for task in all_tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Add a pet first, then you can assign tasks to it.")

st.divider()

st.subheader("Build Schedule")
st.caption("This button now calls the scheduler that reads tasks from the owner's pets.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    plan_text = scheduler.explain_plan()
    st.text(plan_text)
