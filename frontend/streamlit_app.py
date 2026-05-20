import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Empathetic AI Assistant", layout="wide")
st.title("Empathetic AI Assistant")
st.caption("Ask questions about your data — I adapt to how you're feeling.")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("Session Info")
    st.code(st.session_state.session_id[:8] + "...", language=None)
    if st.button("Clear Conversation"):
        requests.delete(f"{API_URL}/session/{st.session_state.session_id}")
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg["role"] == "assistant":
            if msg.get("tone") == "frustrated":
                st.caption("Empathetic mode active")
            score = msg.get("retrieval_score", 0)
            tone = msg.get("tone", "neutral")
            grounding = msg.get("grounding", {})
            st.caption(
                f"Retrieval confidence: {score:.2f} | "
                f"Tone: {tone} | "
                f"Hallucination risk: {grounding.get('hallucination_risk', 'N/A')}"
            )

if prompt := st.chat_input("Ask anything about your data..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("Thinking..."):
        try:
            resp = requests.post(
                f"{API_URL}/chat",
                json={"session_id": st.session_state.session_id, "message": prompt},
                timeout=30,
            )
            resp.raise_for_status()
            data = resp.json()
        except Exception as e:
            st.error(f"Error contacting backend: {e}")
            st.stop()

    with st.chat_message("assistant"):
        st.write(data["answer"])

        col1, col2, col3 = st.columns([1, 1, 6])
        msg_idx = len(st.session_state.messages)
        with col1:
            if st.button("👍", key=f"up_{msg_idx}"):
                requests.post(f"{API_URL}/feedback", json={
                    "session_id": st.session_state.session_id,
                    "message_id": str(msg_idx),
                    "rating": 1,
                })
        with col2:
            if st.button("👎", key=f"down_{msg_idx}"):
                requests.post(f"{API_URL}/feedback", json={
                    "session_id": st.session_state.session_id,
                    "message_id": str(msg_idx),
                    "rating": 0,
                })

        if data.get("tone_detected") == "frustrated":
            st.caption("Empathetic mode active")

        score = data.get("retrieval_score", 0)
        grounding = data.get("grounding", {})
        st.caption(
            f"Retrieval confidence: {score:.2f} | "
            f"Tone: {data.get('tone_detected', 'neutral')} | "
            f"Hallucination risk: {grounding.get('hallucination_risk', 'N/A')}"
        )

    st.session_state.messages.append({
        "role": "assistant",
        "content": data["answer"],
        "tone": data.get("tone_detected"),
        "retrieval_score": data.get("retrieval_score", 0),
        "grounding": data.get("grounding", {}),
    })
