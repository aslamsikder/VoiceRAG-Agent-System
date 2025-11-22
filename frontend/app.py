import streamlit as st
import requests
import json

# Configuration
API_URL = "http://localhost:8000/process_voice/"

st.set_page_config(page_title="VoiceRAG Agent System", layout="wide")

st.title("Voice-Enabled AI Agent")

# --- 1. Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "run_id" not in st.session_state:
    st.session_state.run_id = 0

def reset_input():
    """Increments run_id to force input widgets to clear after sending."""
    st.session_state.run_id += 1

def clear_history():
    """Clears the chat history."""
    st.session_state.messages = []
    reset_input()

# --- 2. Sidebar (Restored) ---
with st.sidebar:
    st.header("📝 Instructions")
    st.markdown("""
    1. **Upload Documents**: Put PDFs/TXTs in `data/` and run ingest.
    2. **Input**: Upload a file or Record live audio.
    3. **Chat**: The history persists below.
    """)
    
    st.divider()
    
    # Button to wipe history if it gets too long
    if st.button("🗑️ Clear Chat History", type="secondary"):
        clear_history()
        st.rerun()

# --- 3. Display Chat History ---
# We loop through history and display messages first
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        
        # If metrics exist (for assistant messages), show them in an expander
        if "metrics" in message:
            with st.expander("📊 Latency Metrics"):
                st.json(message["metrics"])

# --- 4. Input Section (Continuous Input Logic) ---
st.divider()
st.subheader("🗣️ Speak or Upload")

# Dynamic Keys: These change when 'run_id' increments, forcing the widgets to empty/reset.
upload_key = f"upload_{st.session_state.run_id}"
record_key = f"record_{st.session_state.run_id}"

# Tabs for cleaner UI
tab1, tab2 = st.tabs(["📁 Upload File", "🎤 Live Record"])
audio_file = None

with tab1:
    uploaded_file = st.file_uploader("Upload Audio", type=['wav', 'mp3'], key=upload_key)
    if uploaded_file:
        audio_file = uploaded_file

with tab2:
    recorded_file = st.audio_input("Record Voice", key=record_key)
    if recorded_file:
        audio_file = recorded_file

# --- 5. Processing Logic ---
if audio_file:
    # Show the audio player so user can listen before sending (Restored Feature)
    st.audio(audio_file)
    
    if st.button("Send Message", type="primary"):
        with st.spinner("Processing..."):
            
            # Prepare API Request
            filename = audio_file.name if hasattr(audio_file, 'name') else "recording.wav"
            mime_type = audio_file.type if hasattr(audio_file, 'type') else "audio/wav"
            files = {"file": (filename, audio_file, mime_type)}
            
            try:
                # Call Backend
                response = requests.post(API_URL, files=files)
                
                if response.status_code == 200:
                    data = response.json()
                    input_text = data.get('input_text', '...')
                    ai_response = data.get('response', '...')
                    metrics = data.get('metrics', {})

                    # A. Add USER message to history
                    st.session_state.messages.append({
                        "role": "user", 
                        "content": f"**Transcribed:** {input_text}"
                    })

                    # B. Add AI message to history
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_response,
                        "metrics": metrics
                    })

                    # C. Trigger Reset (This clears the input box for the next turn)
                    reset_input()
                    
                    # D. Rerun app to update chat and show empty input
                    st.rerun()
                    
                else:
                    st.error(f"Server Error: {response.text}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")