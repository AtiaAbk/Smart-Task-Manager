import streamlit as st
from datetime import datetime as dt

# CONFIG
st.set_page_config(page_title="Smart Task Manager", page_icon="🗂️")

# STATE INIT
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# HEADER
st.title("🗂️ Smart Task Manager")
st.caption(f"⏰ Current Time: {dt.now().strftime('%d %b %Y, %I:%M:%S %p')}")
st.markdown("---")

# PARSER
def parse_datetime(date, time_input):
    formats = [
        "%Y-%m-%d %H:%M",
        "%d/%m/%Y %H:%M",
        "%Y-%m-%d %I:%M %p",
        "%d/%m/%Y %I:%M %p"
    ]
    combined = f"{date} {time_input}"
    for fmt in formats:
        try:
            return dt.strptime(combined, fmt)
        except:
            pass
    return None

# ADD TASK UI
st.subheader("➕ Add Task")

task_name = st.text_input("Task Name", key="input_name")
task_date = st.text_input("Date (YYYY-MM-DD or DD/MM/YYYY)", key="input_date")
task_time = st.text_input("Time (HH:MM or HH:MM AM/PM)", key="input_time")

if st.button("Add Task"):
    task_dt = parse_datetime(task_date, task_time)
    if not task_name:
        st.warning("Enter task name")
    elif not task_dt:
        st.error("Invalid date/time format")
    elif task_dt < dt.now():
        st.error("Cannot add past task")
    else:
        st.session_state.tasks.append({
            "name": task_name,
            "datetime": task_dt,
            "done": False
        })
        
        del st.session_state["input_name"]
        del st.session_state["input_date"]
        del st.session_state["input_time"]
        st.success("Task added successfully!")
        st.rerun()

st.markdown("---")

# TASK LIST
st.subheader("📋 Tasks")
if not st.session_state.tasks:
    st.info("No tasks yet")

for i, task in enumerate(st.session_state.tasks):
    status = "✔ Done" if task["done"] else "⏳ Pending"
    st.markdown(f"""
### {i+1}. {task['name']}
🕒 {task['datetime'].strftime("%d %b %Y, %I:%M %p")}
**Status:** {status}
""")
    col1, col2 = st.columns(2)
    with col1:
        if not task["done"]:
            
            if st.button("Done ✔", key=f"d{i}"):
                st.session_state.tasks[i]["done"] = True
                st.rerun()
    with col2:
       
        if st.button("Delete 🗑", key=f"x{i}"):
            st.session_state.tasks.pop(i)
            st.rerun()
    st.markdown("---")
