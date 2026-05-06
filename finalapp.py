import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import sqlite3


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

st.set_page_config(page_title="Task Dashboard", layout="centered")

st.title("📋 Smart Task Manager")
st.write("🕒", get_current_time().strftime("%B %d %Y, %I:%M %p"))

st.divider()


st.subheader("➕ Add Task")

with st.form("task_form"):
    name = st.text_input("Task Name")
    date = st.date_input("Date")

    time_input = st.time_input(
        "Time",
        step=timedelta(minutes=1)
    )

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
                st.success("Task saved!")

st.divider()


tasks = get_tasks()


st.subheader("📌 Task List")

if not tasks:
    st.info("No tasks found.")
else:
    for task in tasks:
        task_id, name, time_str, done_flag = task
        status = get_task_status(task)

        col1, col2 = st.columns([3, 2])

        with col1:
            st.write(f"**{name}**")
            st.caption(time_str)

        with col2:
            st.write(status)

            colA, colB = st.columns(2)
            with colA:
                if not done_flag:
                    if st.button("✅", key=f"d{task_id}"):
                        mark_done_db(task_id)
                        st.rerun()
            with colB:
                if st.button("🗑", key=f"x{task_id}"):
                    delete_task_db(task_id)
                    st.rerun()

st.divider()


st.subheader("📊 Overview")

total = len(tasks)
done = sum(1 for t in tasks if t[3] == 1)
expired = sum(1 for t in tasks if t[3] == 0 and datetime.strptime(t[2], "%Y-%m-%d %H:%M:%S") < get_current_time())
pending = total - done - expired

st.metric("Total Tasks", total)
st.metric("Done", done)
st.metric("Pending", pending)
st.metric("Expired", expired)

st.divider()


st.subheader("📈 Task Analytics")

if total > 0:
    df = pd.DataFrame({
        "Status": ["Done", "Pending", "Expired"],
        "Count": [done, pending, expired]
    })
    st.bar_chart(df.set_index("Status"))
else:
    st.info("No data yet.")
