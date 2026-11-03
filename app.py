"""Rootz - team decisions and employee requests, kept in one place.

Run:  streamlit run app.py
"""
import html
import json
import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="Rootz", page_icon="🌱", layout="wide")

BASE = Path(__file__).parent
DATA = BASE / "rootz_data.json"
UPLOADS = BASE / "uploads"
UPLOADS.mkdir(exist_ok=True)

BADGES = {
    "Pending": ("#8a5a00", "#fdf0c9"),
    "Approved": ("#14693f", "#d4f0df"),
    "Accepted": ("#14693f", "#d4f0df"),
    "Rejected": ("#a12b2b", "#fadcdc"),
}
CATEGORIES = ["Salary review", "Leave", "Equipment", "Festival / decorations",
              "Project need", "Other"]


# ----------------------------------------------------------------- data layer
def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def pretty(ts):
    return datetime.strptime(ts, "%Y-%m-%d %H:%M").strftime("%d %b %Y, %H:%M")


def new_id():
    return uuid.uuid4().hex[:8]


def seed():
    return {
        "users": [
            {"id": "head", "name": "Raman", "role": "Head"},
            {"id": "mgr", "name": "Arjun", "role": "Manager"},
            {"id": "e1", "name": "Priya", "role": "Employee"},
            {"id": "e2", "name": "Rahul", "role": "Employee"},
            {"id": "e3", "name": "Sana", "role": "Employee"},
            {"id": "e4", "name": "Dev", "role": "Employee"},
        ],
        "decisions": [
            {"id": "d1", "author": "e1", "title": "Add cold coffee to the menu from December",
             "body": "Customers keep asking for it after 2 PM and we lose them to the shop next door. "
                     "I can make a test batch with the current machine.",
             "created": "2026-10-27 11:20", "status": "Approved", "decided_by": "mgr",
             "decided_at": "2026-10-27 16:45", "note": "Good idea. Start with a two-week trial.",
             "attachments": [],
             "replies": [
                 {"by": "e2", "time": "2026-10-27 12:05",
                  "text": "Kitchen can prep the syrup in advance, no extra work.", "attachments": []},
                 {"by": "e3", "time": "2026-10-27 13:30",
                  "text": "I'll add it to the counter menu once it's approved.", "attachments": []}]},
            {"id": "d2", "author": "e2", "title": "Smaller lunch menu on weekdays",
             "body": "We throw away a lot of unsold food by 3 PM. Cutting from 12 dishes to 7 should "
                     "reduce waste and speed up orders.",
             "created": "2026-11-01 17:10", "status": "Pending", "decided_by": None,
             "decided_at": None, "note": "", "attachments": [],
             "replies": [{"by": "mgr", "time": "2026-11-02 09:30",
                          "text": "How much food was wasted last week? Please attach your notes.",
                          "attachments": []}]},
            {"id": "d3", "author": "mgr", "title": "Close 30 minutes earlier on Sundays",
             "body": "Footfall drops after 7:30 PM on Sundays. New closing time is 8:30 PM instead of 9:00.",
             "created": "2026-10-20 09:30", "status": "Approved", "decided_by": "mgr",
             "decided_at": "2026-10-20 09:30", "note": "", "attachments": [], "replies": []},
            {"id": "d4", "author": "e4", "title": "Free delivery on all orders",
             "body": "Free delivery would bring in more orders from the nearby apartments.",
             "created": "2026-10-30 15:00", "status": "Rejected", "decided_by": "mgr",
             "decided_at": "2026-10-31 10:15",
             "note": "Delivery costs are too high right now. Let's try free delivery above a minimum order first.",
             "attachments": [], "replies": []},
            {"id": "d5", "author": "e3", "title": "Daily opening checklist by the door",
             "body": "Twice last week we opened late because the oven wasn't switched on early. "
                     "A simple checklist will fix that.",
             "created": "2026-10-24 18:00", "status": "Approved", "decided_by": "mgr",
             "decided_at": "2026-10-25 09:10", "note": "Yes, please set it up this week.",
             "attachments": [], "replies": []},
            {"id": "d6", "author": "e2",
             "deleted": {"by": "mgr", "at": "2026-10-29 18:00"}},
        ],
        "requests": [
            {"id": "r1", "by": "e3", "category": "Project need",
             "title": "Loyalty stamp card for regular customers",
             "body": "Regulars come 3-4 times a week. A simple stamp card (10th coffee free) would keep "
                     "them coming back instead of trying the new place.",
             "created": "2026-10-25 12:10", "status": "Rejected", "decided_by": "mgr",
             "decided_at": "2026-10-26 09:00",
             "note": "Not now, we're focused on the cold coffee trial. Send it again in January with a cost estimate.",
             "attachments": [], "replies": []},
            {"id": "r2", "by": "e4", "category": "Leave", "title": "Leave 12-14 Nov",
             "body": "Family function. I'll hand over my deliveries before leaving.",
             "created": "2026-11-02 18:20", "status": "Pending", "decided_by": None,
             "decided_at": None, "note": "", "attachments": [],
             "replies": [{"by": "mgr", "time": "2026-11-03 09:00",
                          "text": "Can you arrange cover for the evening deliveries?",
                          "attachments": []}]},
            {"id": "r3", "by": "e1", "category": "Equipment", "title": "Replace the milk frother",
             "body": "The frother is losing steam pressure and slows down orders at peak time.",
             "created": "2026-10-15 10:00", "status": "Accepted", "decided_by": "mgr",
             "decided_at": "2026-10-16 11:30", "note": "Approved. Order one within the usual budget.",
             "attachments": [], "replies": []},
            {"id": "r4", "by": "e2", "category": "Salary review",
             "title": "Salary review after one year",
             "body": "I've completed one year in the kitchen and taken on opening duties. "
                     "I'd like to discuss a review.",
             "created": "2026-11-02 20:00", "status": "Pending", "decided_by": None,
             "decided_at": None, "note": "", "attachments": [],
             "replies": [{"by": "mgr", "time": "2026-11-03 09:15",
                          "text": "Let's talk on Friday. Please list what you've taken on this year.",
                          "attachments": []}]},
        ],
        "messages": [
            {"thread": "e1", "from": "mgr", "time": "2026-10-27 17:00",
             "text": "Great work on the cold coffee idea, Priya."},
            {"thread": "e1", "from": "e1", "time": "2026-10-27 17:20",
             "text": "Thanks! I'll test the recipe tomorrow morning."},
        ],
        "log": [],
    }


def save(db):
    DATA.write_text(json.dumps(db, indent=2))


def load():
    if DATA.exists():
        return json.loads(DATA.read_text())
    db = seed()
    save(db)
    return db


def save_files(files):
    out = []
    for f in files or []:
        safe = Path(f.name).name
        p = UPLOADS / f"{new_id()}_{safe}"
        p.write_bytes(f.getbuffer())
        out.append({"name": safe, "path": str(p)})
    return out


def delete_files(item):
    atts = list(item.get("attachments", []))
    for r in item.get("replies", []):
        atts += r.get("attachments", [])
    for a in atts:
        Path(a["path"]).unlink(missing_ok=True)


db = load()
users = {u["id"]: u for u in db["users"]}

st.session_state.setdefault("me", "mgr")
st.session_state.setdefault("sel", "mgr")
st.session_state.setdefault("del_id", None)
st.session_state.setdefault("reset_confirm", False)


def nm(i):
    u = users.get(i)
    return f"{u['name']} ({u['role']})" if u else "Unknown"


def badge(status):
    fg, bg = BADGES[status]
    return (f'<span style="color:{fg};background:{bg};padding:2px 10px;border-radius:999px;'
            f'font-size:0.8rem;font-weight:600">{status}</span>')


# ------------------------------------------------------------------ styling
BUBBLES = [(60, 5, 18, 0), (30, 15, 22, 3), (90, 25, 26, 6), (40, 38, 20, 2),
           (70, 50, 24, 8), (25, 62, 19, 1), (100, 72, 28, 4), (45, 85, 21, 7),
           (35, 92, 23, 5), (55, 45, 30, 10), (20, 8, 17, 9), (80, 58, 27, 12)]
bubble_html = "".join(
    f'<div class="bubble" style="width:{s}px;height:{s}px;left:{l}%;'
    f'animation-duration:{d}s;animation-delay:-{dl}s"></div>'
    for s, l, d, dl in BUBBLES)

st.markdown(f"""
<style>
.stApp {{background: linear-gradient(160deg,#f3faf5 0%,#e4f3e9 55%,#d6ecde 100%);}}
.block-container {{position: relative; z-index: 1; padding-top: 2rem; max-width: 1250px;}}
.bubble {{position: fixed; bottom: -130px; border-radius: 50%; pointer-events: none; z-index: 0;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,.85), rgba(110,200,155,.22));
  border: 1px solid rgba(70,160,115,.25); animation: rise linear infinite;}}
@keyframes rise {{from {{transform: translateY(0);}} to {{transform: translateY(-125vh);}}}}
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button
  {{border-radius: 999px;}}
[data-testid="stVerticalBlockBorderWrapper"] {{background: rgba(255,255,255,.72);
  border-radius: 16px; border-color: #bfe0cc;}}
.tree {{position: relative; height: 120px;}}
.tree .stem {{position:absolute; left:50%; top:0; width:3px; height:22px; background:#3a8f66;
  transform: translateX(-1.5px); border-radius: 2px;}}
.tree .bar {{position:absolute; top:22px; height:3px; background:#3a8f66; border-radius: 2px;}}
.tree .drops {{position:absolute; top:22px; left:0; right:0; bottom:0; display:flex;}}
.tree .col {{flex:1; position:relative;}}
.tree .drop {{position:absolute; left:50%; top:0; bottom:0; width:3px; background:
  linear-gradient(#3a8f66,#8cc9a8); transform: translateX(-1.5px); border-radius: 2px;}}
</style>
{bubble_html}
""", unsafe_allow_html=True)

# ------------------------------------------------------------------ sidebar
with st.sidebar:
    st.markdown("## 🌱 Rootz")
    st.caption("Decisions and requests, rooted in one place.")
    me_id = st.selectbox("Viewing as", [u["id"] for u in db["users"]], format_func=nm, key="me")
    st.caption("Prototype switcher. A real version would use sign-in.")
    me = users[me_id]
    is_mgr = me["role"] == "Manager"
    is_head = me["role"] == "Head"

    if is_mgr:
        st.divider()
        st.markdown("**Manager controls**")
        if not st.session_state.reset_confirm:
            if st.button("🔄 Reset all decisions"):
                st.session_state.reset_confirm = True
                st.rerun()
        else:
            st.warning("⚠️ This will permanently delete ALL decisions, their discussions and "
                       "attachments. It cannot be undone. Only a record of the reset remains.")
            if st.button("Yes, reset everything", type="primary"):
                for d in db["decisions"]:
                    delete_files(d)
                db["decisions"] = []
                db["log"].append({"type": "reset", "by": me["id"], "at": now()})
                save(db)
                st.session_state.reset_confirm = False
                st.rerun()
            if st.button("Cancel"):
                st.session_state.reset_confirm = False
                st.rerun()

# --------------------------------------------------------------------- tree
st.markdown("# 🌱 Rootz")
st.caption("Demo data. Use 'Viewing as' in the sidebar to try each role: Manager, Head or Employee.")
head = next((u for u in db["users"] if u["role"] == "Head"), None)
if head:
    st.caption(f"🏢 Head of company: **{head['name']}**, can see every request, including rejected ones.")

mgr = next(u for u in db["users"] if u["role"] == "Manager")
emps = [u for u in db["users"] if u["role"] == "Employee"]


def select(i):
    st.session_state.sel = i


def node(u, key):
    st.button(f"{'🌳' if u['role'] == 'Manager' else '🌱'} {u['name']}", key=key,
              use_container_width=True, on_click=select, args=(u["id"],),
              type="primary" if st.session_state.sel == u["id"] else "secondary")


top = st.columns([2, 1, 2])
with top[1]:
    node(mgr, "node_mgr")
if emps:
    pad = 50 / len(emps)
    drops = "".join('<div class="col"><div class="drop"></div></div>' for _ in emps)
    st.markdown(f'<div class="tree"><div class="stem"></div>'
                f'<div class="bar" style="left:{pad}%;right:{pad}%"></div>'
                f'<div class="drops">{drops}</div></div>', unsafe_allow_html=True)
    for col, u in zip(st.columns(len(emps)), emps):
        with col:
            node(u, f"node_{u['id']}")

if is_mgr or is_head:
    with st.expander("➕ Add an employee (grow the roots)"):
        with st.form("add_emp", clear_on_submit=True):
            new_name = st.text_input("Employee name", key="ae_name")
            if st.form_submit_button("Add employee", key="ae_submit"):
                if new_name.strip():
                    db["users"].append({"id": "e" + new_id(), "name": new_name.strip(),
                                        "role": "Employee"})
                    save(db)
                    st.rerun()

st.write("")


# -------------------------------------------------------------- shared pieces
def show_files(files, key):
    for i, a in enumerate(files or []):
        p = Path(a["path"])
        if p.exists():
            st.download_button(f"📎 {a['name']}", p.read_bytes(), file_name=a["name"],
                               key=f"dl_{key}_{i}")


def show_replies(item, key):
    for n, r in enumerate(item["replies"]):
        u = users.get(r["by"])
        with st.chat_message("user", avatar="🌳" if u and u["role"] == "Manager" else "🌱"):
            st.markdown(f"**{nm(r['by'])}** · {pretty(r['time'])}")
            if r["text"]:
                st.write(r["text"])
            show_files(r.get("attachments"), f"{key}_r{n}")


def reply_form(item, key, label="Reply"):
    with st.form(f"rf_{key}", clear_on_submit=True):
        txt = st.text_area("Reply", key=f"rt_{key}", height=80, label_visibility="collapsed",
                           placeholder="Write a reply or ask a question...")
        files = st.file_uploader("Attach files", accept_multiple_files=True, key=f"rfu_{key}")
        if st.form_submit_button(label, key=f"rs_{key}"):
            if txt.strip() or files:
                item["replies"].append({"by": me["id"], "time": now(), "text": txt.strip(),
                                        "attachments": save_files(files)})
                save(db)
                st.rerun()


def outcome(item, noun):
    if item["status"] in ("Approved", "Accepted"):
        msg = f"✅ {item['status']} by {nm(item['decided_by'])} on {pretty(item['decided_at'])}"
        if item.get("note"):
            msg += f"\n\n“{item['note']}”"
        st.success(msg)
    elif item["status"] == "Rejected":
        msg = f"❌ Rejected by {nm(item['decided_by'])} on {pretty(item['decided_at'])}"
        if item.get("note"):
            msg += f"\n\nReason: {item['note']}"
        st.error(msg)


def decide_controls(item, key, yes, kind):
    """Manager approve/reject with written explanation."""
    with st.expander("⚖️ Review and decide", expanded=True):
        note = st.text_area("Written explanation (required to reject)", key=f"n_{key}", height=80)
        a, b = st.columns(2)
        if a.button(f"✅ {yes}", key=f"ap_{key}", use_container_width=True):
            item.update(status=yes, decided_by=me["id"], decided_at=now(), note=note.strip())
            save(db)
            st.rerun()
        if b.button("❌ Reject", key=f"rj_{key}", use_container_width=True):
            if not note.strip():
                st.error("Please write a reason before rejecting.")
            else:
                item.update(status="Rejected", decided_by=me["id"], decided_at=now(),
                            note=note.strip())
                save(db)
                st.rerun()


def start_delete(i):
    st.session_state.del_id = i


def clear_delete():
    st.session_state.del_id = None


# ---------------------------------------------------------------- decisions
def render_decision(d, where):
    k = f"{where}_d_{d['id']}"
    with st.container(border=True):
        if d.get("deleted"):
            st.markdown(f"🗑️ **Decision deleted** by **{nm(d['deleted']['by'])}** "
                        f"on {pretty(d['deleted']['at'])}")
            return
        st.markdown(f"**{html.escape(d['title'])}** &nbsp; {badge(d['status'])}",
                    unsafe_allow_html=True)
        st.caption(f"By {nm(d['author'])} · {pretty(d['created'])}")
        st.write(d["body"])
        show_files(d.get("attachments"), k)
        outcome(d, "decision")
        with st.expander(f"💬 Discussion ({len(d['replies'])})"):
            show_replies(d, k)
            reply_form(d, k)
        if is_mgr:
            if d["status"] == "Pending":
                decide_controls(d, k, "Approved", "decision")
            if st.session_state.del_id == d["id"]:
                st.warning("⚠️ This will permanently delete this decision, its discussion and "
                           "attachments. Only a note of who deleted it and when will remain.")
                c1, c2 = st.columns(2)
                if c1.button("Yes, delete permanently", key=f"dy_{k}", type="primary"):
                    did, author = d["id"], d["author"]
                    delete_files(d)
                    d.clear()
                    d.update(id=did, author=author, deleted={"by": me["id"], "at": now()})
                    save(db)
                    st.session_state.del_id = None
                    st.rerun()
                c2.button("Cancel", key=f"dc_{k}", on_click=clear_delete)
            else:
                st.button("🗑️ Delete decision", key=f"dd_{k}", on_click=start_delete,
                          args=(d["id"],))


def matches(item, q):
    q = q.lower().strip()
    if not q:
        return True
    blob = " ".join([item.get("title", ""), item.get("body", "")] +
                    [r["text"] for r in item.get("replies", [])]).lower()
    return q in blob


def tab_all_decisions():
    last_reset = next((e for e in reversed(db["log"]) if e["type"] == "reset"), None)
    if last_reset:
        st.info(f"ℹ️ All decisions were reset by {nm(last_reset['by'])} "
                f"on {pretty(last_reset['at'])}.")
    c1, c2 = st.columns([2, 1])
    q = c1.text_input("Search decisions", key="q_dec", placeholder="Search titles, details, replies")
    status = c2.selectbox("Status", ["All", "Pending", "Approved", "Rejected"], key="f_dec")
    shown = 0
    for d in reversed(db["decisions"]):
        if d.get("deleted"):
            if status == "All" and not q.strip():
                render_decision(d, "R")
                shown += 1
            continue
        if (status == "All" or d["status"] == status) and matches(d, q):
            render_decision(d, "R")
            shown += 1
    if not shown:
        st.caption("No decisions match.")


def tab_new_decision():
    if is_head:
        st.info("The Head has oversight access. Decisions are posted by the manager and employees.")
        return
    st.caption("Attach proof (meeting minutes, an email, a document) so anyone who joins later "
               "can see why this was decided." +
               ("" if is_mgr else " Your manager will approve or reject it."))
    with st.form("new_decision", clear_on_submit=True):
        title = st.text_input("Decision title", key="nd_title")
        body = st.text_area("Details and reasoning", key="nd_body", height=120)
        files = st.file_uploader("Attach proof or documents", accept_multiple_files=True,
                                 key="nd_files")
        if st.form_submit_button("Publish decision", key="nd_submit"):
            if not title.strip() or not body.strip():
                st.error("Please add a title and details.")
            else:
                t = now()
                db["decisions"].append({
                    "id": new_id(), "author": me["id"], "title": title.strip(),
                    "body": body.strip(), "created": t,
                    "status": "Approved" if is_mgr else "Pending",
                    "decided_by": me["id"] if is_mgr else None,
                    "decided_at": t if is_mgr else None, "note": "",
                    "attachments": save_files(files), "replies": []})
                save(db)
                st.rerun()


# ----------------------------------------------------------------- requests
def can_see(r):
    return me["role"] in ("Manager", "Head") or r["by"] == me["id"]


def render_request(r, where):
    if not can_see(r):
        return
    k = f"{where}_r_{r['id']}"
    with st.container(border=True):
        st.markdown(f"**{html.escape(r['title'])}** &nbsp; {badge(r['status'])}",
                    unsafe_allow_html=True)
        st.caption(f"{r['category']} · from {nm(r['by'])} · {pretty(r['created'])}")
        st.write(r["body"])
        show_files(r.get("attachments"), k)
        outcome(r, "request")
        with st.expander(f"💬 Conversation ({len(r['replies'])})"):
            show_replies(r, k)
            reply_form(r, k)
        if is_mgr and r["status"] == "Pending":
            decide_controls(r, k, "Accepted", "request")


def tab_requests():
    if is_head:
        st.info("Head view: every request is listed here with the manager's explanation, "
                "including rejected ones.")
    elif is_mgr:
        st.caption("All employee requests. Ask questions in the conversation, then accept or reject "
                   "with a written explanation.")
    else:
        st.caption("Only you, your manager and the Head can see your requests.")
    c1, c2 = st.columns([2, 1])
    q = c1.text_input("Search requests", key="q_req")
    status = c2.selectbox("Status", ["All", "Pending", "Accepted", "Rejected"], key="f_req")
    shown = 0
    for r in reversed(db["requests"]):
        if can_see(r) and (status == "All" or r["status"] == status) and matches(r, q):
            render_request(r, "R")
            shown += 1
    if not shown:
        st.caption("No requests match.")


def tab_new_request():
    if me["role"] != "Employee":
        st.info("Requests are sent by employees to their manager.")
        return
    st.caption(f"Sent privately to {mgr['name']} (visible to the Head as well).")
    with st.form("new_request", clear_on_submit=True):
        cat = st.selectbox("Type of request", CATEGORIES, key="nr_cat")
        title = st.text_input("Title", key="nr_title")
        body = st.text_area("What do you need and why?", key="nr_body", height=120)
        files = st.file_uploader("Attach supporting files (optional)", accept_multiple_files=True,
                                 key="nr_files")
        if st.form_submit_button("Send request", key="nr_submit"):
            if not title.strip() or not body.strip():
                st.error("Please add a title and details.")
            else:
                db["requests"].append({
                    "id": new_id(), "by": me["id"], "category": cat, "title": title.strip(),
                    "body": body.strip(), "created": now(), "status": "Pending",
                    "decided_by": None, "decided_at": None, "note": "",
                    "attachments": save_files(files), "replies": []})
                save(db)
                st.rerun()


# ----------------------------------------------------------------- messages
def tab_messages():
    if is_head:
        st.info("Direct messages are private between the manager and each employee.")
        return
    if is_mgr:
        target = st.selectbox("Message an employee", [u["id"] for u in emps],
                              format_func=nm, key="dm_target")
    else:
        target = me["id"]
        st.caption(f"Private chat with your manager, {mgr['name']}.")
    for m in [m for m in db["messages"] if m["thread"] == target]:
        with st.chat_message("user", avatar="🌳" if m["from"] == mgr["id"] else "🌱"):
            st.markdown(f"**{nm(m['from'])}** · {pretty(m['time'])}")
            st.write(m["text"])
    with st.form("dm_form", clear_on_submit=True):
        txt = st.text_input("Message", key="dm_text", label_visibility="collapsed",
                            placeholder="Write a private message...")
        if st.form_submit_button("Send", key="dm_submit") and txt.strip():
            db["messages"].append({"thread": target, "from": me["id"], "text": txt.strip(),
                                   "time": now()})
            save(db)
            st.rerun()


# ------------------------------------------------------------------- layout
left, right = st.columns([1, 1.5], gap="large")

with left:
    sel = users[st.session_state.sel]
    st.markdown(f"#### {'🌳' if sel['role'] == 'Manager' else '🌱'} {sel['name']}'s decisions")
    st.caption(f"{sel['role']} · shared decision threads")
    mine = [d for d in reversed(db["decisions"]) if d.get("author") == sel["id"]]
    if not mine:
        st.caption("No decisions shared yet.")
    for d in mine:
        render_decision(d, "L")

with right:
    t1, t2, t3, t4, t5 = st.tabs(["🌱 Decisions", "➕ New decision", "📨 Requests",
                                  "✉️ New request", "💌 Messages"])
    with t1:
        tab_all_decisions()
    with t2:
        tab_new_decision()
    with t3:
        tab_requests()
    with t4:
        tab_new_request()
    with t5:
        tab_messages()