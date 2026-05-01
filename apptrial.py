import streamlit as st
from datetime import datetime
import pandas as pd

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Task Dashboard", layout="wide")

# -----------------------------
# SESSION STATE
# -----------------------------
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_current_time():
    return datetime.now()

def get_task_status(task):
    now = get_current_time()
    if task["done"]:
        return "✅ Done"
    elif task["time"] < now:
        return "❌ Expired"
    else:
        return "⏳ Pending"

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("📋 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Add Task"])

st.sidebar.markdown("---")
st.sidebar.write("🕒", get_current_time().strftime("%I:%M %p"))

# -----------------------------
# ADD TASK PAGE
# -----------------------------
if page == "Add Task":
    st.title("➕ Add New Task")

    with st.form("task_form"):
        name = st.text_input("Task Name")

        col1, col2 = st.columns(2)
        with col1:
            date = st.date_input("Date")
        with col2:
            time_input = st.time_input("Time")

        submitted = st.form_submit_button("Add Task")

        if submitted:
            if not name:
                st.error("Task name required!")
            else:
                task_datetime = datetime.combine(date, time_input)

                if task_datetime < get_current_time():
                    st.error("Time already passed!")
                else:
                    st.session_state.tasks.append({
                        "task": name,
                        "time": task_datetime,
                        "done": False
                    })
                    st.success("Task Added!")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
else:
    st.title("📊 Dashboard")

    tasks = st.session_state.tasks

    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    expired = sum(1 for t in tasks if not t["done"] and t["time"] < get_current_time())
    pending = total - done - expired

    # -----------------------------
    # METRIC CARDS
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total", total)
    col2.metric("Done", done)
    col3.metric("Pending", pending)
    col4.metric("Expired", expired)

    st.divider()

    # -----------------------------
    # CHART
    # -----------------------------
    if total > 0:
        df = pd.DataFrame({
            "Status": ["Done", "Pending", "Expired"],
            "Count": [done, pending, expired]
        })
        st.bar_chart(df.set_index("Status"))
    else:
        st.info("No tasks yet.")

    st.divider()

    # -----------------------------
    # TASK LIST
    # -----------------------------
    st.subheader("📌 Tasks")

    if not tasks:
        st.info("No tasks available.")
    else:
        for i, task in enumerate(tasks):
            status = get_task_status(task)
            time_str = task["time"].strftime("%Y-%m-%d %I:%M %p")

            col1, col2, col3, col4 = st.columns([4, 3, 2, 2])

            with col1:
                st.write(f"**{task['task']}**")
            with col2:
                st.write(time_str)
            with col3:
                st.write(status)
            with col4:
                if not task["done"]:
                    if st.button("✅", key=f"d{i}"):
                        st.session_state.tasks[i]["done"] = True
                        st.rerun()

                if st.button("🗑", key=f"x{i}"):
                    st.session_state.tasks.pop(i)
                    st.rerun()