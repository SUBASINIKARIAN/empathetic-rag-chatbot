import streamlit as st
import requests
import uuid
from datetime import datetime

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="EmpathAI — Workplace Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    min-height: 100vh;
}

/* ── Header ── */
.app-header {
    display: flex; align-items: center; gap: 14px;
    padding: 18px 0 8px 0;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 20px;
}
.app-header .logo { font-size: 2.2rem; }
.app-header h1 {
    font-size: 1.6rem; font-weight: 700; margin: 0;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.app-header p { color: #94a3b8; font-size: 0.85rem; margin: 0; }

/* ── Chat bubbles ── */
.msg-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: #fff; padding: 14px 18px;
    border-radius: 18px 18px 4px 18px;
    margin: 6px 0 6px 60px;
    box-shadow: 0 4px 15px rgba(79,70,229,0.3);
    font-size: 0.95rem; line-height: 1.6;
}
.msg-bot {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #e2e8f0; padding: 14px 18px;
    border-radius: 18px 18px 18px 4px;
    margin: 6px 60px 6px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    font-size: 0.95rem; line-height: 1.6;
}
.msg-label { font-size: 0.72rem; font-weight: 600; letter-spacing: 0.05em; margin-bottom: 4px; text-transform: uppercase; }
.msg-label-user { color: #a78bfa; text-align: right; margin-right: 4px; }
.msg-label-bot  { color: #60a5fa; }
.msg-time { font-size: 0.68rem; color: #64748b; margin-top: 4px; }
.msg-time-right { text-align: right; }

/* ── Badges ── */
.badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 0.72rem; font-weight: 600; margin: 2px 3px; letter-spacing: 0.04em;
}
.badge-frustrated { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.3); }
.badge-confused   { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }
.badge-neutral    { background: rgba(34,197,94,0.15);  color: #4ade80; border: 1px solid rgba(34,197,94,0.3); }
.badge-empathy    { background: rgba(167,139,250,0.15); color: #c4b5fd; border: 1px solid rgba(167,139,250,0.3); }
.metrics-row { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-top: 10px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(15,15,26,0.95) !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
.sidebar-stat {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 10px; padding: 12px 16px; margin-bottom: 10px; text-align: center;
}
.sidebar-stat .val {
    font-size: 1.6rem; font-weight: 700;
    background: linear-gradient(90deg, #a78bfa, #60a5fa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sidebar-stat .lbl { font-size: 0.72rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Recommended question cards ── */
.rec-section-label {
    font-size: 0.7rem; font-weight: 600; color: #64748b;
    text-transform: uppercase; letter-spacing: 0.1em; margin: 14px 0 8px;
}

/* ── Divider ── */
.chat-divider { border: none; border-top: 1px solid rgba(255,255,255,0.05); margin: 8px 0; }

/* ── Thinking ── */
.thinking-dot {
    display: inline-block; width: 7px; height: 7px; border-radius: 50%;
    background: #a78bfa; animation: blink 1.2s infinite; margin: 0 2px;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }
@keyframes blink { 0%,80%,100%{opacity:0.2} 40%{opacity:1} }

/* ── Hide streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
div[data-testid="stChatMessage"] { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ── Recommendation engine ─────────────────────────────────────────────────────
TOPIC_RECOMMENDATIONS: dict[str, list[tuple[str, str]]] = {
    "leave": [
        ("🤒", "How do I apply for sick leave?"),
        ("👶", "What is the parental leave policy?"),
        ("📅", "Can I carry over unused PTO to next year?"),
        ("🧘", "How do I use a mental health day?"),
    ],
    "mental_health": [
        ("📞", "Is EAP counseling completely confidential?"),
        ("🧠", "How many mental health days am I entitled to?"),
        ("💬", "How do I talk to my manager about stress?"),
        ("🛋️", "What happens during an EAP counseling session?"),
    ],
    "remote": [
        ("💻", "What home office equipment does the company provide?"),
        ("🕐", "What are the core working hours for remote employees?"),
        ("✈️", "Can I work remotely from another country?"),
        ("🏢", "How many days per week do I need to come to the office?"),
    ],
    "burnout": [
        ("🆘", "What support is available if I am burned out?"),
        ("📉", "How do I reduce my workload temporarily?"),
        ("🧘", "What wellness resources does the company offer?"),
        ("👩‍💼", "Can my manager help me manage burnout?"),
    ],
    "ai": [
        ("🔒", "What data can I NOT enter into AI tools?"),
        ("✅", "Is ChatGPT approved for company use?"),
        ("⚖️", "Who owns content I create with AI tools?"),
        ("🎓", "Where can I learn more about using AI at work?"),
    ],
    "benefits": [
        ("🏥", "What health insurance plans are available?"),
        ("💰", "How does the 401k company match work?"),
        ("📚", "What is the learning and development budget?"),
        ("🚌", "How do I claim commuter benefits?"),
    ],
    "default": [
        ("🏖️", "How many leave days do I get per year?"),
        ("🏥", "How do I access EAP counseling?"),
        ("🏠", "Can I work remotely full-time?"),
        ("🤖", "What AI tools are approved at work?"),
    ],
}


def get_recommendations(question: str) -> list[tuple[str, str]]:
    q = question.lower()
    if any(w in q for w in ["leave", "pto", "vacation", "sick", "parental", "days off", "time off"]):
        return TOPIC_RECOMMENDATIONS["leave"]
    if any(w in q for w in ["eap", "counseling", "mental health", "therapy", "stress", "anxiety", "wellness"]):
        return TOPIC_RECOMMENDATIONS["mental_health"]
    if any(w in q for w in ["remote", "work from home", "hybrid", "office", "wfh", "internet", "equipment"]):
        return TOPIC_RECOMMENDATIONS["remote"]
    if any(w in q for w in ["burnout", "burned out", "exhausted", "overwhelmed", "tired", "recharge"]):
        return TOPIC_RECOMMENDATIONS["burnout"]
    if any(w in q for w in ["ai", "gemini", "chatgpt", "copilot", "artificial intelligence", "llm", "tool"]):
        return TOPIC_RECOMMENDATIONS["ai"]
    if any(w in q for w in ["benefit", "insurance", "health plan", "401k", "retirement", "stipend", "salary"]):
        return TOPIC_RECOMMENDATIONS["benefits"]
    return TOPIC_RECOMMENDATIONS["default"]


# ── Session State ─────────────────────────────────────────────────────────────
if "session_id"    not in st.session_state: st.session_state.session_id    = str(uuid.uuid4())
if "messages"      not in st.session_state: st.session_state.messages      = []
if "total_queries" not in st.session_state: st.session_state.total_queries = 0
if "thumbs_up"     not in st.session_state: st.session_state.thumbs_up     = 0
if "thumbs_down"   not in st.session_state: st.session_state.thumbs_down   = 0
if "tone_counts"   not in st.session_state: st.session_state.tone_counts   = {"neutral": 0, "frustrated": 0, "confused": 0}
if "last_question" not in st.session_state: st.session_state.last_question = ""

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🧠 EmpathAI")
    st.markdown("<div style='color:#64748b;font-size:0.8rem;margin-bottom:18px;'>Workplace Wellness Assistant</div>", unsafe_allow_html=True)

    # Stats
    st.markdown("### Session Stats")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""<div class='sidebar-stat'>
            <div class='val'>{st.session_state.total_queries}</div>
            <div class='lbl'>Queries</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        total_fb = st.session_state.thumbs_up + st.session_state.thumbs_down
        sat = round(st.session_state.thumbs_up / total_fb * 100) if total_fb else 0
        st.markdown(f"""<div class='sidebar-stat'>
            <div class='val'>{sat}%</div>
            <div class='lbl'>Satisfaction</div>
        </div>""", unsafe_allow_html=True)

    # Tone breakdown
    st.markdown("### Tone Breakdown")
    for tone, emoji, color in [("neutral", "😊", "#4ade80"), ("frustrated", "😤", "#f87171"), ("confused", "🤔", "#fbbf24")]:
        count = st.session_state.tone_counts.get(tone, 0)
        pct = round(count / max(st.session_state.total_queries, 1) * 100)
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;margin:6px 0;'>
            <span style='color:#94a3b8;font-size:0.8rem;'>{emoji} {tone.title()}</span>
            <span style='color:{color};font-weight:600;font-size:0.85rem;'>{count} ({pct}%)</span>
        </div>""", unsafe_allow_html=True)

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)

    # Dynamic recommendations
    recs = get_recommendations(st.session_state.last_question)
    label = "Recommended Questions" if st.session_state.last_question else "Quick Start Questions"
    st.markdown(f"<div class='rec-section-label'>{label}</div>", unsafe_allow_html=True)

    for icon, text in recs:
        if st.button(f"{icon}  {text}", key=f"rec_{text}", use_container_width=True):
            st.session_state["prefill"] = text
            st.rerun()

    st.markdown("<hr style='border-color:rgba(255,255,255,0.06);margin:16px 0;'>", unsafe_allow_html=True)

    if st.button("🗑️ Clear Conversation", use_container_width=True):
        try:
            requests.delete(f"{API_URL}/session/{st.session_state.session_id}", timeout=5)
        except Exception:
            pass
        for key in ["messages", "session_id", "total_queries", "thumbs_up", "thumbs_down", "last_question"]:
            del st.session_state[key]
        st.session_state.tone_counts = {"neutral": 0, "frustrated": 0, "confused": 0}
        st.rerun()

    st.markdown(f"""
    <div style='margin-top:16px;padding:10px;background:rgba(255,255,255,0.03);border-radius:8px;'>
        <div style='font-size:0.68rem;color:#475569;font-family:monospace;'>
            Session: {st.session_state.session_id[:12]}...
        </div>
    </div>""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class='app-header'>
    <div class='logo'>🧠</div>
    <div>
        <h1>EmpathAI Workplace Assistant</h1>
        <p>Ask anything about HR policies, mental health, remote work, or benefits — I adapt to how you feel.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def tone_badge(tone: str) -> str:
    icons = {"frustrated": "😤", "confused": "🤔", "neutral": "😊"}
    icon = icons.get(tone, "😊")
    css = f"badge-{tone}" if tone in ("frustrated", "confused", "neutral") else "badge-neutral"
    return f"<span class='badge {css}'>{icon} {tone.title()}</span>"


def render_history():
    for i, msg in enumerate(st.session_state.messages):
        ts = msg.get("time", "")
        if msg["role"] == "user":
            st.markdown("<div class='msg-label msg-label-user'>You</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='msg-user'>{msg['content']}<div class='msg-time msg-time-right'>{ts}</div></div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='msg-label msg-label-bot'>🧠 EmpathAI</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='msg-bot'>{msg['content']}<div class='msg-time'>{ts}</div></div>", unsafe_allow_html=True)

            tone = msg.get("tone", "neutral")
            badges = tone_badge(tone)
            if tone == "frustrated":
                badges += "<span class='badge badge-empathy'>💜 Empathetic Mode</span>"
            st.markdown(f"<div class='metrics-row'>{badges}</div>", unsafe_allow_html=True)

            fb_col1, fb_col2, _ = st.columns([1, 1, 8])
            with fb_col1:
                if st.button("👍", key=f"up_{i}", help="Helpful"):
                    requests.post(f"{API_URL}/feedback", json={
                        "session_id": st.session_state.session_id,
                        "message_id": str(i), "rating": 1,
                    }, timeout=5)
                    st.session_state.thumbs_up += 1
                    st.toast("Thanks for the feedback!", icon="👍")
            with fb_col2:
                if st.button("👎", key=f"down_{i}", help="Not helpful"):
                    requests.post(f"{API_URL}/feedback", json={
                        "session_id": st.session_state.session_id,
                        "message_id": str(i), "rating": 0,
                    }, timeout=5)
                    st.session_state.thumbs_down += 1
                    st.toast("Got it, I'll try to do better.", icon="👎")

        st.markdown("<hr class='chat-divider'>", unsafe_allow_html=True)


# ── Empty state ───────────────────────────────────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
    <div style='text-align:center;padding:60px 20px 30px;'>
        <div style='font-size:3.5rem;margin-bottom:16px;'>🧠</div>
        <div style='font-size:1.2rem;font-weight:600;color:#e2e8f0;margin-bottom:8px;'>How can I help you today?</div>
        <div style='color:#64748b;font-size:0.9rem;max-width:480px;margin:0 auto 30px;'>
            I'm here to help with HR policies, mental health resources, remote work guidelines, and more.
            I'll adjust my tone based on how you're feeling.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    suggestions = [
        ("🏖️", "How many leave days do I get?"),
        ("🧘", "I'm feeling really burned out"),
        ("🏠", "Can I work remotely full-time?"),
        ("🤖", "What AI tools are approved at work?"),
        ("🏥", "How do I access the EAP counseling?"),
        ("😤", "I don't understand the leave policy at all"),
    ]
    for col, (icon, text) in zip([c1, c2, c3, c1, c2, c3], suggestions):
        with col:
            if st.button(f"{icon} {text}", key=f"home_{text}", use_container_width=True):
                st.session_state["prefill"] = text
                st.rerun()
else:
    render_history()

# ── Chat input ────────────────────────────────────────────────────────────────
prefill = st.session_state.pop("prefill", None)
prompt = st.chat_input("Ask about leave, mental health, remote work, benefits...") or prefill

if prompt:
    now = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": now})
    st.session_state.total_queries += 1
    st.session_state.last_question = prompt  # update for sidebar recommendations

    thinking_placeholder = st.empty()
    thinking_placeholder.markdown("""
    <div class='msg-label msg-label-bot'>🧠 EmpathAI</div>
    <div class='msg-bot' style='color:#64748b;'>
        <span class='thinking-dot'></span>
        <span class='thinking-dot'></span>
        <span class='thinking-dot'></span>
        &nbsp; Thinking...
    </div>
    """, unsafe_allow_html=True)

    try:
        resp = requests.post(
            f"{API_URL}/chat",
            json={"session_id": st.session_state.session_id, "message": prompt},
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        thinking_placeholder.empty()
        st.error(f"Could not reach backend: {e}")
        st.stop()

    thinking_placeholder.empty()

    tone = data.get("tone_detected", "neutral")
    st.session_state.tone_counts[tone] = st.session_state.tone_counts.get(tone, 0) + 1

    st.session_state.messages.append({
        "role": "assistant",
        "content": data["answer"],
        "tone": tone,
        "time": datetime.now().strftime("%I:%M %p"),
    })

    st.rerun()
