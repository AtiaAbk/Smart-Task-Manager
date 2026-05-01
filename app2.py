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
# SESSION STATE
# ─────────────────────────────────────────────
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "action" not in st.session_state:
    st.session_state.action = None
if "action_id" not in st.session_state:
    st.session_state.action_id = None

def get_status(task):
    if task["done"]:
        return "Completed"
    elif datetime.fromisoformat(task["deadline"]) < datetime.now():
        return "Expired"
    return "Pending"

# Process actions from previous run
if st.session_state.action == "done" and st.session_state.action_id:
    for t in st.session_state.tasks:
        if t["id"] == st.session_state.action_id:
            t["done"] = True
    st.session_state.action = None
    st.session_state.action_id = None

if st.session_state.action == "delete" and st.session_state.action_id:
    st.session_state.tasks = [t for t in st.session_state.tasks if t["id"] != st.session_state.action_id]
    st.session_state.action = None
    st.session_state.action_id = None

reschedule_id = None
if st.session_state.action == "reschedule" and st.session_state.action_id:
    reschedule_id = st.session_state.action_id
    st.session_state.action = None
    st.session_state.action_id = None

# ─────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap');

*, *::before, *::after { box-sizing: border-box; }

:root {
    --bg:       #1b2a3b;
    --card:     #1f3248;
    --card2:    #243a55;
    --inp:      #162434;
    --nav:      #111e2b;
    --teal:     #2dd4bf;
    --teal2:    #14b8a6;
    --text:     #dde6f0;
    --muted:    #7fa1be;
    --dim:      #3f6080;
    --brd:      #264060;
    --red:      #ef4444;
    --yellow:   #f59e0b;
    --green:    #22c55e;
}

.stApp {
    background: var(--bg) !important;
    font-family: 'DM Sans', sans-serif !important;
    color: var(--text) !important;
}

/* Hide chrome */
#MainMenu, footer, header, .stDeployButton,
[data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

/* ── NAVBAR ── */
.navbar {
    background: var(--nav);
    border-bottom: 1px solid var(--brd);
    padding: 12px 36px;
    display: flex;
    justify-content: flex-end;
    gap: 22px;
}
.ni { font-size: 20px; opacity: .65; cursor: pointer; }
.ni:hover, .ni.on { opacity: 1; }

/* ── PAGE ── */
.wrap { padding: 32px 36px 48px; }

/* ── TITLE ── */
.app-hd { display:flex; align-items:center; gap:16px; margin-bottom:36px; }
.app-hd .ico { font-size:52px; filter:drop-shadow(0 6px 14px rgba(0,0,0,.5)); }
.app-hd h1 {
    font-family:'Syne',sans-serif;
    font-size:38px; font-weight:800;
    color:var(--text); letter-spacing:-.5px; line-height:1;
}
.app-hd p { font-size:13px; color:var(--muted); margin-top:3px; }

/* ── SECTION TITLE ── */
.stitle {
    font-family:'Syne',sans-serif;
    font-size:21px; font-weight:700;
    color:var(--text); margin-bottom:14px;
}

/* ── CARD ── */
.card {
    background:var(--card);
    border:1px solid var(--brd);
    border-radius:13px;
    padding:20px 22px;
    margin-bottom:16px;
}
.ctag {
    font-family:'Space Mono',monospace;
    font-size:10px; font-weight:700;
    color:var(--dim); letter-spacing:2.5px;
    margin-bottom:14px;
}

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stDateInput > div > div > input,
.stTimeInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--inp) !important;
    border: 1px solid var(--brd) !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
}
.stTextInput > div > div > input:focus,
.stDateInput > div > div > input:focus,
.stTimeInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--teal) !important;
    box-shadow: 0 0 0 2px rgba(45,212,191,.12) !important;
}
.stTextInput label, .stDateInput label,
.stTimeInput label, .stTextArea label {
    color: var(--muted) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder { color: var(--dim) !important; }

/* Radio */
.stRadio > label { color: var(--muted) !important; font-size: 13px !important; }
.stRadio label span { color: var(--muted) !important; font-size: 13px !important; }

/* ── BUTTONS ── */
.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    border-radius: 8px !important;
    transition: all .18s !important;
    border: none !important;
}

/* Primary teal */
.bprimary .stButton > button {
    background: var(--teal) !important;
    color: #071a14 !important;
    width: 100% !important;
    padding: 13px 20px !important;
    font-size: 15px !important;
    box-shadow: 0 4px 18px rgba(45,212,191,.3) !important;
}
.bprimary .stButton > button:hover {
    background: var(--teal2) !important;
    box-shadow: 0 6px 24px rgba(45,212,191,.45) !important;
    transform: translateY(-1px) !important;
}

/* Complete */
.bcomplete .stButton > button {
    background: var(--teal) !important;
    color: #071a14 !important;
    width: 100% !important;
    font-size: 11px !important;
    letter-spacing: 1.2px !important;
    padding: 10px !important;
}

/* Outline */
.boutline .stButton > button {
    background: transparent !important;
    color: var(--muted) !important;
    border: 1px solid var(--brd) !important;
    width: 100% !important;
    font-size: 11px !important;
    letter-spacing: 1.2px !important;
    padding: 10px !important;
}
.boutline .stButton > button:hover {
    border-color: var(--teal) !important;
    color: var(--teal) !important;
}

/* Mark Done */
.bdone .stButton > button {
    background: rgba(45,212,191,.07) !important;
    color: var(--teal) !important;
    border: 1px solid rgba(45,212,191,.2) !important;
    font-size: 11px !important;
    padding: 5px 8px !important;
    width: 100% !important;
}
.bdone .stButton > button:hover { background: rgba(45,212,191,.16) !important; }

/* Delete */
.bdel .stButton > button {
    background: rgba(239,68,68,.07) !important;
    color: var(--red) !important;
    border: 1px solid rgba(239,68,68,.18) !important;
    font-size: 14px !important;
    padding: 4px 8px !important;
    width: 100% !important;
}
.bdel .stButton > button:hover { background: rgba(239,68,68,.16) !important; }

/* Edit */
.bedit .stButton > button {
    background: rgba(127,161,190,.07) !important;
    color: var(--muted) !important;
    border: 1px solid rgba(127,161,190,.18) !important;
    font-size: 14px !important;
    padding: 4px 8px !important;
    width: 100% !important;
}
.bedit .stButton > button:hover { color: var(--teal) !important; }

/* ── TASK CARD ── */
.tcard {
    background: var(--card2);
    border: 1px solid var(--brd);
    border-left: 3px solid var(--brd);
    border-radius: 10px;
    padding: 13px 15px 9px;
    margin-bottom: 8px;
    transition: border-left-color .2s;
}
.tcard:hover { border-left-color: var(--teal); }
.tcard-top { display:flex; justify-content:space-between; align-items:flex-start; }
.tname { font-family:'Syne',sans-serif; font-size:16px; font-weight:700; color:var(--text); }
.tmeta { font-size:11px; color:var(--dim); margin:4px 0 3px; }

/* ── BADGES / CHIPS ── */
.badge {
    display:inline-block; padding:3px 9px;
    border-radius:20px; font-size:10px; font-weight:700;
    font-family:'Space Mono',monospace; white-space:nowrap;
}
.b-low    { background:rgba(59,130,246,.14); color:#60a5fa; }
.b-med    { background:rgba(245,158,11,.14); color:#fbbf24; }
.b-high   { background:rgba(239,68,68,.14);  color:#f87171; }

.chip {
    display:inline-block; padding:3px 9px;
    border-radius:5px; font-size:10px; font-weight:700;
    font-family:'Space Mono',monospace; margin-top:4px;
}
.c-exp  { background:#dc2626; color:#fff; }
.c-pnd  { background:#b45309; color:#fff; }
.c-done { background:#15803d; color:#fff; }

/* ── FOCUS ── */
.fname {
    font-family:'Syne',sans-serif;
    font-size:26px; font-weight:800; color:var(--text);
}
.frow { display:flex; align-items:center; gap:12px; margin-bottom:10px; }

/* ── STATS ── */
.sbar {
    background: var(--nav);
    border: 1px solid var(--brd);
    border-radius: 9px;
    padding: 12px 18px;
    text-align: center;
    font-family: 'Space Mono', monospace;
    font-size: 11px; color: var(--muted);
    margin-top: 12px;
    letter-spacing: .3px;
}
.sbar b { color: var(--text); }

/* ── MISC ── */
.divl { height:1px; background:var(--brd); margin:12px 0; }
.flbl { font-size:12px; color:var(--muted); margin-bottom:6px; font-weight:500; }
.empty { text-align:center; color:var(--dim); font-size:13px; padding:28px 0; }

/* Column gap */
div[data-testid="column"] { padding: 0 8px !important; }

/* Scrollbar */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:var(--bg); }
::-webkit-scrollbar-thumb { background:var(--brd); border-radius:3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def pbadge(p):
    c = {"Low":"b-low","Medium":"b-med","High":"b-high"}.get(p,"b-low")
    return f'<span class="badge {c}">{p}</span>'

def schip(s):
    c = {"Expired":"c-exp","Pending":"c-pnd","Completed":"c-done"}.get(s,"c-pnd")
    return f'<span class="chip {c}">{s}</span>'

def S(n): return f'<div style="height:{n}px"></div>'

def get_focus():
    exp = [t for t in st.session_state.tasks if get_status(t)=="Expired"]
    pnd = [t for t in st.session_state.tasks if get_status(t)=="Pending"]
    arr = exp or pnd or st.session_state.tasks
    return arr[0] if arr else None

# ─────────────────────────────────────────────
# NAVBAR
# ─────────────────────────────────────────────
st.markdown("""
<div class="navbar">
    <span class="ni on">🏠</span>
    <span class="ni">📅</span>
    <span class="ni">⚙️</span>
    <span class="ni">👤</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PAGE WRAP
# ─────────────────────────────────────────────
st.markdown('<div class="wrap">', unsafe_allow_html=True)

# APP TITLE
st.markdown("""
<div class="app-hd">
    <span class="ico">📁</span>
    <div>
        <h1>Smart Task Manager</h1>
        <p>productivity app</p>
    </div>
</div>
""", unsafe_allow_html=True)

# TWO COLUMNS
L, R = st.columns(2, gap="large")

# ══════════════════════════════════════════════
# LEFT
# ══════════════════════════════════════════════
with L:
    st.markdown('<div class="stitle">Task Entry &amp; Focus</div>', unsafe_allow_html=True)

    # CREATE NEW TASK card header
    st.markdown('<div class="card"><div class="ctag">＋ &nbsp;CREATE NEW TASK</div></div>', unsafe_allow_html=True)

    # Prefill if rescheduling
    prefill = None
    if reschedule_id:
        prefill = next((t for t in st.session_state.tasks if t["id"]==reschedule_id), None)
        if prefill:
            st.info(f"🔄 Rescheduling: **{prefill['task']}**")

    task_name = st.text_input("Task Name",
        value=prefill["task"] if prefill else "",
        placeholder="Enter task name...")

    cd, ct = st.columns(2)
    with cd: task_date = st.date_input("Date", value=date.today())
    with ct: task_time_v = st.time_input("Time", value=time(12,0))

    priority = st.radio("Priority", ["Low","Medium","High"], horizontal=True)

    st.markdown(S(8), unsafe_allow_html=True)
    st.markdown('<div class="bprimary">', unsafe_allow_html=True)
    if st.button("Add Task" if not prefill else "✓ Update Schedule",
                 use_container_width=True, key="add_btn"):
        if task_name.strip():
            dl = datetime.combine(task_date, task_time_v).isoformat()
            if prefill:
                prefill["deadline"] = dl
                prefill["done"] = False
                st.success("✅ Rescheduled!")
            else:
                st.session_state.tasks.append({
                    "id": str(uuid.uuid4()),
                    "task": task_name.strip(),
                    "deadline": dl,
                    "priority": priority,
                    "done": False,
                    "description": ""
                })
                st.success("✅ Task added!")
            st.rerun()
        else:
            st.error("⚠️ Enter a task name.")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(S(22), unsafe_allow_html=True)

    # FOCUS VIEW
    st.markdown('<div class="card"><div class="ctag">🎯 &nbsp;FOCUS VIEW</div></div>', unsafe_allow_html=True)

    focus = get_focus()
    if focus:
        fs = get_status(focus)
        st.markdown(f"""
        <div class="frow">
            <div class="fname">{focus['task']}</div>
            {schip(fs)}
        </div>
        <div style="font-size:13px;color:var(--muted);margin-bottom:5px;font-weight:500;">Description</div>
        """, unsafe_allow_html=True)

        desc = st.text_area("Desc", value=focus.get("description",""),
                            placeholder="Add a note...",
                            label_visibility="collapsed",
                            key=f"d_{focus['id']}", height=85)
        focus["description"] = desc

        st.markdown(S(8), unsafe_allow_html=True)
        f1, f2 = st.columns(2)
        with f1:
            st.markdown('<div class="bcomplete">', unsafe_allow_html=True)
            if st.button("✓ MARK COMPLETE", key="fc", use_container_width=True):
                focus["done"] = True
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        with f2:
            st.markdown('<div class="boutline">', unsafe_allow_html=True)
            if st.button("RESCHEDULE", key="fr", use_container_width=True):
                st.session_state.action = "reschedule"
                st.session_state.action_id = focus["id"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty">🎉 No pending tasks. Add one above!</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════
# RIGHT
# ══════════════════════════════════════════════
with R:
    st.markdown('<div class="stitle">Detailed Task List</div>', unsafe_allow_html=True)
    st.markdown('<div class="card"><div class="ctag">TASK OVERVIEW</div></div>', unsafe_allow_html=True)

    srch = st.text_input("S", placeholder="🔍  Search tasks...", label_visibility="collapsed")

    st.markdown(S(6), unsafe_allow_html=True)
    st.markdown('<div class="flbl">Filters:</div>', unsafe_allow_html=True)
    flt = st.radio("F", ["All","Pending","Completed","Expired"],
                   horizontal=True, label_visibility="collapsed", key="flt")

    st.markdown('<div class="divl"></div>', unsafe_allow_html=True)

    tasks = st.session_state.tasks
    if flt != "All":
        tasks = [t for t in tasks if get_status(t)==flt]
    if srch:
        tasks = [t for t in tasks if srch.lower() in t["task"].lower()]

    if not tasks:
        st.markdown('<div class="empty">No tasks found.</div>', unsafe_allow_html=True)
    else:
        for task in tasks:
            st_ = get_status(task)
            dl = datetime.fromisoformat(task["deadline"])
            ts = dl.strftime("%d %b %Y, %I:%M %p")

            st.markdown(f"""
            <div class="tcard">
                <div class="tcard-top">
                    <div class="tname">{task['task']}</div>
                    {pbadge(task['priority'])}
                </div>
                <div class="tmeta">🕐 {ts}</div>
                {schip(st_)}
            </div>
            """, unsafe_allow_html=True)

            a1, a2, a3 = st.columns([4,1,1])
            with a1:
                if st_ != "Completed":
                    st.markdown('<div class="bdone">', unsafe_allow_html=True)
                    if st.button("✓ Mark Done", key=f"dn_{task['id']}", use_container_width=True):
                        st.session_state.action = "done"
                        st.session_state.action_id = task["id"]
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
            with a2:
                st.markdown('<div class="bdel">', unsafe_allow_html=True)
                if st.button("🗑", key=f"dl_{task['id']}", use_container_width=True):
                    st.session_state.action = "delete"
                    st.session_state.action_id = task["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with a3:
                st.markdown('<div class="bedit">', unsafe_allow_html=True)
                if st.button("✏️", key=f"ed_{task['id']}", use_container_width=True):
                    st.session_state.action = "reschedule"
                    st.session_state.action_id = task["id"]
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            st.markdown(S(4), unsafe_allow_html=True)

    # Stats
    all_t = st.session_state.tasks
    total = len(all_t)
    done_ = sum(1 for t in all_t if t["done"])
    exp_  = sum(1 for t in all_t if get_status(t)=="Expired")
    pnd_  = sum(1 for t in all_t if get_status(t)=="Pending")

    st.markdown(f"""
    <div class="sbar">
        Total Tasks: <b>{total}</b> &nbsp;|&nbsp;
        Completed: <b>{done_}</b> &nbsp;|&nbsp;
        Pending: <b>{pnd_}</b> &nbsp;|&nbsp;
        Expired: <b>{exp_}</b>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
