import streamlit as st
from datetime import datetime
import pandas as pd
import sqlite3

# -----------------------------
# DB SETUP
# -----------------------------
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT,
    time TEXT,
    done INTEGER
)
""")
conn.commit()

# -----------------------------
# FUNCTIONS
# -----------------------------
def get_current_time():
    return datetime.now()

def get_task_status(task):
    now = get_current_time()
    task_time = datetime.strptime(task[2], "%Y-%m-%d %H:%M:%S")

    if task[3]:
        return "✅ Done"
    elif task_time < now:
        return "❌ Expired"
    else:
        return "⏳ Pending"

def add_task_db(name, task_time):
    c.execute("INSERT INTO tasks (task, time, done) VALUES (?, ?, ?)",
              (name, task_time, 0))
    conn.commit()

def get_tasks():
    c.execute("SELECT * FROM tasks ORDER BY time ASC")
    return c.fetchall()

def mark_done_db(task_id):
    c.execute("UPDATE tasks SET done=1 WHERE id=?", (task_id,))
    conn.commit()

def delete_task_db(task_id):
    c.execute("DELETE FROM tasks WHERE id=?", (task_id,))
    conn.commit()

# -----------------------------
# UI CONFIG
# -----------------------------
st.set_page_config(page_title="Task Dashboard", layout="wide")

st.title("📊 Smart Task Manager (Persistent)")
st.write("🕒", get_current_time().strftime("%B %d %Y, %I:%M %p"))

st.divider()

# -----------------------------
# ADD TASK
# -----------------------------
st.subheader("➕ Add Task")

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
                add_task_db(name, task_datetime.strftime("%Y-%m-%d %H:%M:%S"))
                st.success("Task saved permanently!")

st.divider()

# -----------------------------
# LOAD TASKS
# -----------------------------
tasks = get_tasks()

# -----------------------------
# STATS
# -----------------------------
total = len(tasks)
done = sum(1 for t in tasks if t[3] == 1)
expired = sum(1 for t in tasks if t[3] == 0 and datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S") < get_current_time())
pending = total - done - expired

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total", total)
col2.metric("Done", done)
col3.metric("Pending", pending)
col4.metric("Expired", expired)

# -----------------------------
# CHART
# -----------------------------
st.subheader("📊 Task Analytics")

if total > 0:
    df = pd.DataFrame({
        "Status": ["Done", "Pending", "Expired"],
        "Count": [done, pending, expired]
    })
    st.bar_chart(df.set_index("Status"))
else:
    st.info("No data yet.")

st.divider()

# -----------------------------
# TASK LIST
# -----------------------------
st.subheader("📌 Task List")

if not tasks:
    st.info("No tasks found.")
else:
    for task in tasks:
        task_id, name, time_str, done_flag = task
        status = get_task_status(task)

        col1, col2, col3, col4 = st.columns([4, 3, 2, 2])

        with col1:
            st.write(f"**{name}**")
        with col2:
            st.write(time_str)
        with col3:
            st.write(status)
        with col4:
            if not done_flag:
                if st.button("✅", key=f"d{task_id}"):
                    mark_done_db(task_id)
                    st.rerun()

            if st.button("🗑", key=f"x{task_id}"):
                delete_task_db(task_id)
                st.rerun()