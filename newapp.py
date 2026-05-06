import streamlit as st
from datetime import datetime


if "tasks" not in st.session_state:
    st.session_state.tasks = []


def get_current_time():
    return datetime.now()

def get_task_status(task):
    now = get_current_time()

    if task["done"]:
        return "✅ Done"
    elif task["time"] < now:
        return "❌ Expired"
    else:
        return "⏳ Not Done"


st.title("📋 Smart Task Manager")
st.write("### 🕒 Current Time:", get_current_time().strftime("%B %d %Y, %I:%M %p"))

st.divider()


st.subheader("➕ Add New Task")

with st.form("task_form"):
    name = st.text_input("Task Name")

    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Select Date")
    with col2:
        time_input = st.time_input("Select Time")

    submitted = st.form_submit_button("Add Task")

    if submitted:
        if not name:
            st.error("Task name cannot be empty!")
        else:
            task_datetime = datetime.combine(date, time_input)
            now = get_current_time()

            if task_datetime < now:
                st.error("Selected time already passed!")
            else:
                st.session_state.tasks.append({
                    "task": name,
                    "time": task_datetime,
                    "done": False
                })
                st.success("Task added successfully!")

st.divider()


st.subheader("📌 Task List")

if not st.session_state.tasks:
    st.info("No tasks available.")
else:
    for i, task in enumerate(st.session_state.tasks):
        status = get_task_status(task)
        time_str = task["time"].strftime("%Y-%m-%d %I:%M %p")

        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])

        with col1:
            st.write(f"**{task['task']}**")

        with col2:
            st.write(time_str)

        with col3:
            st.write(status)

        with col4:
            if not task["done"]:
                if st.button(f"✅ Done {i}", key=f"done_{i}"):
                    st.session_state.tasks[i]["done"] = True
                    st.rerun()

            if st.button(f"🗑 Delete {i}", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.rerun()
