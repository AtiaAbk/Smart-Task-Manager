import streamlit as st
from datetime import datetime, date, time
import uuid

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Task Manager",
    page_icon="📁",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Dark Theme matching the design
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
    --bg-primary:    #1a2332;
    --bg-card:       #1e2d3d;
    --bg-card2:      #243447;
    --bg-input:      #1a2332;
    --accent-teal:   #2dd4bf;
    --accent-teal2:  #14b8a6;
    --text-primary:  #e2e8f0;
    --text-muted:    #94a3b8;
    --text-dim:      #64748b;
    --border:        #2d4059;
    --expired:       #ef4444;
    --pending:       #f59e0b;
    --completed:     #22c55e;
    --low:           #3b82f6;
    --medium:        #f59e0b;
    --high:          #ef4444;
    --nav-bg:        #111827;
}

/* ── App wrapper ── */
.stApp {
    background: var(--bg-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none; }

/* ── Top Navigation Bar ── */
.nav-bar {
    background: var(--nav-bg);
    padding: 14px 32px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    gap: 28px;
    border-bottom: 1px solid #1f2937;
    position: sticky;
    top: 0;
    z-index: 100;
}
.nav-icon {
    color: var(--text-muted);
    font-size: 20px;
    cursor: pointer;
    transition: color 0.2s;
    padding: 6px;
    border-radius: 8px;
}
.nav-icon:hover { color: var(--accent-teal); }
.nav-icon.active { color: var(--text-primary); }

/* ── Main Content ── */
.main-content {
    padding: 32px 36px 40px 36px;
}

/* ── App Header ── */
.app-header {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 36px;
}
.app-header .folder-icon {
    font-size: 52px;
    line-height: 1;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.4));
}
.app-header .title-block h1 {
    font-family: 'Syne', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: var(--text-primary);
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.app-header .title-block p {
    font-size: 14px;
    color: var(--text-muted);
    font-weight: 400;
    margin-top: 2px;
    letter-spacing: 0.5px;
}

/* ── Two-column layout ── */
.two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 28px;
    align-items: start;
}

/* ── Section Title ── */
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 20px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 14px;
    letter-spacing: -0.3px;
}

/* ── Cards ── */
.card {
    background: var(--bg-card);
    border-radius: 14px;
    padding: 24px;
    border: 1px solid var(--border);
    margin-bottom: 16px;
}
.card-header-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    gap: 6px;
}

/* ── Form Labels ── */
.form-label {
    font-size: 13px;
    color: var(--text-muted);
    margin-bottom: 6px;
    font-weight: 500;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    padding: 10px 14px !important;
}
.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus,
.stTimeInput > div > div > input:focus {
    border-color: var(--accent-teal) !important;
    box-shadow: 0 0 0 2px rgba(45,212,191,0.15) !important;
}
.stTextInput label, .stDateInput label, .stTimeInput label,
.stTextArea label, .stSelectbox label {
    color: var(--text-muted) !important;
    font-size: 13px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 500 !important;
}

/* ── Buttons ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    letter-spacing: 0.5px !important;
    transition: all 0.2s !important;
    border: none !important;
}
.btn-add > button {
    background: var(--accent-teal) !important;
    color: #0f1923 !important;
    width: 100% !important;
    padding: 13px !important;
    font-size: 15px !important;
}
.btn-add > button:hover {
    background: var(--accent-teal2) !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(45,212,191,0.35) !important;
}
.btn-complete > button {
    background: var(--accent-teal) !important;
    color: #0f1923 !important;
    width: 100% !important;
    font-size: 12px !important;
    letter-spacing: 1.5px !important;
    padding: 10px !important;
}
.btn-reschedule > button {
    background: transparent !important;
    color: var(--text-muted) !important;
    border: 1px solid var(--border) !important;
    width: 100% !important;
    font-size: 12px !important;
    letter-spacing: 1.5px !important;
    padding: 10px !important;
}
.btn-reschedule > button:hover {
    border-color: var(--accent-teal) !important;
    color: var(--accent-teal) !important;
}

/* ── Priority badges ── */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}
.badge-low      { background: rgba(59,130,246,0.18); color: #60a5fa; }
.badge-medium   { background: rgba(245,158,11,0.18); color: #fbbf24; }
.badge-high     { background: rgba(239,68,68,0.18);  color: #f87171; }

/* ── Status chips ── */
.chip {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.5px;
    font-family: 'Space Mono', monospace;
    margin-top: 6px;
}
.chip-expired   { background: var(--expired);  color: white; }
.chip-pending   { background: rgba(245,158,11,0.85); color: #1a1a00; }
.chip-completed { background: rgba(34,197,94,0.85);  color: #0a1a0a; }

/* ── Task cards in list ── */
.task-card {
    background: var(--bg-card2);
    border-radius: 10px;
    padding: 16px 18px;
    margin-bottom: 10px;
    border-left: 3px solid transparent;
    display: flex;
    flex-direction: column;
    gap: 6px;
    transition: border-color 0.2s;
}
.task-card:hover { border-left-color: var(--accent-teal); }
.task-card-title {
    font-family: 'Syne', sans-serif;
    font-size: 16px;
    font-weight: 700;
    color: var(--text-primary);
}
.task-card-meta {
    font-size: 12px;
    color: var(--text-dim);
    display: flex;
    align-items: center;
    gap: 5px;
}
.task-card-row {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
}
.task-card-actions {
    display: flex;
    align-items: center;
    gap: 6px;
    margin-top: 6px;
}
.action-btn {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 6px;
    color: var(--text-muted);
    cursor: pointer;
    padding: 5px 10px;
    font-size: 11px;
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    transition: all 0.15s;
    display: inline-flex;
    align-items: center;
    gap: 4px;
}
.action-btn:hover { color: var(--accent-teal); border-color: var(--accent-teal); }
.action-btn.danger:hover { color: var(--expired); border-color: var(--expired); }

/* ── Filter pills ── */
.filter-bar {
    display: flex;
    gap: 6px;
    margin-bottom: 14px;
    flex-wrap: wrap;
}
.filter-pill {
    padding: 5px 14px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border);
    background: transparent;
    color: var(--text-muted);
    font-family: 'DM Sans', sans-serif;
    transition: all 0.15s;
}
.filter-pill.active {
    background: var(--accent-teal);
    color: #0f1923;
    border-color: var(--accent-teal);
}

/* ── Task overview label ── */
.overview-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
}
.overview-label {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    color: var(--text-dim);
    letter-spacing: 2px;
    font-weight: 700;
}

/* ── Focus view ── */
.focus-task-name {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text-primary);
    margin-bottom: 8px;
}

/* ── Stats bar ── */
.stats-bar {
    background: var(--nav-bg);
    padding: 14px 24px;
    border-radius: 10px;
    text-align: center;
    font-size: 13px;
    color: var(--text-muted);
    margin-top: 14px;
    border: 1px solid var(--border);
    font-family: 'Space Mono', monospace;
    letter-spacing: 0.5px;
}
.stats-bar span { color: var(--text-primary); font-weight: 700; }

/* ── Divider ── */
.hr { border: none; border-top: 1px solid var(--border); margin: 16px 0; }

/* ── Streamlit column gap fix ── */
div[data-testid="column"] { padding: 0 8px !important; }
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }

/* ── Radio override for priority ── */
.stRadio label { color: var(--text-muted) !important; font-size: 13px !important; }
.stRadio > div { flex-direction: row !important; gap: 16px !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Alert / success messages ── */
.stAlert { border-radius: 8px !important; }

/* Responsive */
@media (max-width: 768px) {
    .two-col { grid-template-columns: 1fr; }
    .main-content { padding: 20px 16px; }
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "filter" not in st.session_state:
    st.session_state.filter = "All"
if "search" not in st.session_state:
    st.session_state.search = ""
if "edit_id" not in st.session_state:
    st.session_state.edit_id = None
if "reschedule_id" not in st.session_state:
    st.session_state.reschedule_id = None


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def get_status(task):
    if task["done"]:
        return "Completed"
    elif task["deadline"] < datetime.now():
        return "Expired"
    return "Pending"

def get_focus_task():
    """Return first non-done task, prioritising expired then pending"""
    expired = [t for t in st.session_state.tasks if get_status(t) == "Expired"]
    pending = [t for t in st.session_state.tasks if get_status(t) == "Pending"]
    return (expired or pending or st.session_state.tasks or [None])[0]

def priority_badge(p):
    cls = {"Low": "badge-low", "Medium": "badge-medium", "High": "badge-high"}.get(p, "badge-low")
    return f'<span class="badge {cls}">{p}</span>'

def status_chip(s):
    cls = {"Expired": "chip-expired", "Pending": "chip-pending", "Completed": "chip-completed"}.get(s, "chip-pending")
    return f'<span class="chip {cls}">{s.upper()}</span>'


# ─────────────────────────────────────────────
# NAV BAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="nav-bar">
    <span class="nav-icon active">🏠</span>
    <span class="nav-icon">📅</span>
    <span class="nav-icon">⚙️</span>
    <span class="nav-icon">👤</span>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT WRAPPER
# ─────────────────────────────────────────────
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# App Header
st.markdown("""
<div class="app-header">
    <div class="folder-icon">📁</div>
    <div class="title-block">
        <h1>Smart Task Manager</h1>
        <p>productivity app</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TWO COLUMNS
# ─────────────────────────────────────────────
left_col, right_col = st.columns(2, gap="large")


# ══════════════════════════════════════════════
# LEFT COLUMN — Task Entry & Focus View
# ══════════════════════════════════════════════
with left_col:
    st.markdown('<div class="section-title">Task Entry &amp; Focus</div>', unsafe_allow_html=True)

    # ── CREATE NEW TASK CARD ──
    st.markdown("""
    <div class="card">
        <div class="card-header-label">＋ &nbsp;CREATE NEW TASK</div>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        # Reschedule mode
        reschedule_task = None
        if st.session_state.reschedule_id:
            reschedule_task = next((t for t in st.session_state.tasks if t["id"] == st.session_state.reschedule_id), None)

        if reschedule_task:
            st.info(f"🔄 Rescheduling: **{reschedule_task['task']}**")

        task_name = st.text_input("Task Name", placeholder="Enter task name...",
                                   value=reschedule_task["task"] if reschedule_task else "")

        c1, c2 = st.columns(2)
        with c1:
            task_date = st.date_input("Date", value=date.today())
        with c2:
            task_time = st.time_input("Time", value=time(12, 0))

        priority = st.radio("Priority", ["Low", "Medium", "High"], horizontal=True)

        st.markdown('<div class="btn-add">', unsafe_allow_html=True)
        if st.button("Add Task" if not reschedule_task else "Update Schedule", use_container_width=True):
            if task_name.strip():
                deadline = datetime.combine(task_date, task_time)
                if reschedule_task:
                    reschedule_task["deadline"] = deadline
                    reschedule_task["done"] = False
                    st.session_state.reschedule_id = None
                    st.success("✅ Task rescheduled!")
                else:
                    st.session_state.tasks.append({
                        "id": str(uuid.uuid4()),
                        "task": task_name.strip(),
                        "deadline": deadline,
                        "priority": priority,
                        "done": False,
                        "description": ""
                    })
                    st.success("✅ Task added!")
                st.rerun()
            else:
                st.error("Please enter a task name.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

    # ── FOCUS VIEW CARD ──
    focus = get_focus_task()
    st.markdown("""
    <div class="card">
        <div class="card-header-label">🎯 &nbsp;FOCUS VIEW</div>
    </div>
    """, unsafe_allow_html=True)

    if focus:
        fs = get_status(focus)
        st.markdown(f"""
        <div style="display:flex; align-items:center; gap:14px; margin-bottom:10px;">
            <div class="focus-task-name">{focus['task']}</div>
            {status_chip(fs)}
        </div>
        <div class="form-label">Description</div>
        """, unsafe_allow_html=True)

        desc_val = st.text_area("Description", value=focus.get("description", ""),
                                 placeholder="Add a description...", label_visibility="collapsed",
                                 key=f"desc_{focus['id']}")
        focus["description"] = desc_val

        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown('<div class="btn-complete">', unsafe_allow_html=True)
            if st.button("✓ MARK COMPLETE", key="focus_done", use_container_width=True):
                focus["done"] = True
                st.success("Task marked complete!")
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with fc2:
            st.markdown('<div class="btn-reschedule">', unsafe_allow_html=True)
            if st.button("RESCHEDULE", key="focus_reschedule", use_container_width=True):
                st.session_state.reschedule_id = focus["id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="color: var(--text-dim); font-size: 14px; text-align: center; padding: 24px 0;">
            🎉 No pending tasks. Add a task to get started!
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
# RIGHT COLUMN — Detailed Task List
# ══════════════════════════════════════════════
with right_col:
    st.markdown('<div class="section-title">Detailed Task List</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="padding-bottom:14px;">
        <div class="overview-row">
            <div class="overview-label">TASK OVERVIEW</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Search
    search_query = st.text_input("Search tasks...", placeholder="🔍  Search tasks...",
                                  label_visibility="collapsed")

    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)

    # Filter pills via radio
    filter_choice = st.radio(
        "Filter",
        ["All", "Pending", "Completed", "Expired"],
        horizontal=True,
        label_visibility="collapsed"
    )
    st.session_state.filter = filter_choice

    st.markdown('<div class="hr"></div>', unsafe_allow_html=True)

    # Filter tasks
    filtered = st.session_state.tasks
    if filter_choice != "All":
        filtered = [t for t in filtered if get_status(t) == filter_choice]
    if search_query:
        filtered = [t for t in filtered if search_query.lower() in t["task"].lower()]

    if not filtered:
        st.markdown("""
        <div style="color: var(--text-dim); font-size: 14px; text-align: center; padding: 32px 0;">
            No tasks found.
        </div>
        """, unsafe_allow_html=True)
    else:
        for task in filtered:
            status = get_status(task)
            time_str = task["deadline"].strftime("%d %b %Y, %I:%M %p")

            st.markdown(f"""
            <div class="task-card">
                <div class="task-card-row">
                    <div class="task-card-title">{task['task']}</div>
                    {priority_badge(task['priority'])}
                </div>
                <div class="task-card-meta">🕐 {time_str}</div>
                {status_chip(status)}
            </div>
            """, unsafe_allow_html=True)

            # Action buttons row
            a1, a2, a3 = st.columns([3, 1, 1])
            with a1:
                if status != "Completed":
                    if st.button(f"✓ Mark Done", key=f"done_{task['id']}"):
                        task["done"] = True
                        st.rerun()
            with a2:
                if st.button("🗑", key=f"del_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != task["id"]]
                    st.rerun()
            with a3:
                if st.button("✏️", key=f"edit_{task['id']}"):
                    st.session_state.reschedule_id = task["id"]
                    st.rerun()

            st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)

    # Stats bar
    total = len(st.session_state.tasks)
    completed = sum(1 for t in st.session_state.tasks if t["done"])
    expired = sum(1 for t in st.session_state.tasks if get_status(t) == "Expired")
    pending = sum(1 for t in st.session_state.tasks if get_status(t) == "Pending")

    st.markdown(f"""
    <div class="stats-bar">
        Total Tasks: <span>{total}</span> &nbsp;|&nbsp;
        Completed: <span>{completed}</span> &nbsp;|&nbsp;
        Pending: <span>{pending}</span> &nbsp;|&nbsp;
        Expired: <span>{expired}</span>
    </div>
    """, unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)  # close main-content