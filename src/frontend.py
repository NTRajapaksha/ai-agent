import streamlit as st
import requests

# Page Config
st.set_page_config(
    page_title="AI Agent Workspace",
    page_icon="🤖",
    layout="wide"
)

# --- Sidebar Configuration ---
with st.sidebar:
    st.title("⚙️ Control Panel")
    st.markdown("---")
    
    # You can add more backend controls here later
    model_type = st.selectbox(
        "AI Model",
        ["Gemini 2.5 Flash", "Gemini Pro (Legacy)"],
        index=0
    )
    
    st.markdown("### Agent Capabilities")
    st.success("✅ Web Search (Tavily)")
    st.success("✅ Report Generation")
    st.success("✅ Memory (LangGraph)")
    
    if st.button("🗑️ Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# --- Main Interface ---
st.title("🤖 Autonomous AI Agent")
st.caption("Powered by LangGraph, FastAPI, and Google Gemini")

# 1. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# 2. Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. User Input
if prompt := st.chat_input("Ask me to research something..."):
    # Add User Message to History
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. Agent Processing
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("🧠 Agent is thinking & searching..."):
            try:
                # Call FastAPI Backend
                response = requests.post(
                    "http://localhost:8000/run-agent", 
                    json={"query": prompt}
                )
                
                if response.status_code == 200:
                    result = response.json().get("response")
                    full_response = result
                else:
                    full_response = f"Error: {response.text}"
                    
            except requests.exceptions.ConnectionError:
                full_response = "❌ Failed to connect to backend. Is the FastAPI server running on port 8000?"

        # Display Response
        message_placeholder.markdown(full_response)
        
    # Add Assistant Message to History
    st.session_state.messages.append({"role": "assistant", "content": full_response})