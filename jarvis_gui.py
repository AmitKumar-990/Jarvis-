import streamlit as st

def set_custom_style():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(45deg, #1a1a1a, #2c3e50);
            color: white;
        }
        
        /* Circular button styling */
        div.stButton > button:first-child {
            border-radius: 50% !important;
            width: 120px !important;
            height: 120px !important;
            padding: 0 !important;
            margin: 2rem auto;
            display: block !important;
            transition: all 0.3s ease !important;
            font-size: 3rem !important;
            border: none !important;
            background: #2ecc71 !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
        }
        
        div.stButton > button:first-child:hover {
            transform: scale(1.1) !important;
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.3) !important;
        }
        
        div.stButton > button:first-child:active {
            transform: scale(0.95) !important;
        }
        
        /* Active state styling */
        .mic-active {
            background: #e74c3c !important;
            animation: pulse 1.5s infinite !important;
        }
        
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(231, 76, 60, 0); }
            100% { box-shadow: 0 0 0 0 rgba(231, 76, 60, 0); }
        }
        
        .status-box {
            padding: 1rem;
            border-radius: 10px;
            text-align: center;
            margin: 2rem auto;
            width: 80%;
            background: #ffffff15;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

def main():
    # Initialize session state
    if 'mic_active' not in st.session_state:
        st.session_state.mic_active = False

    # Page configuration
    st.set_page_config(
        page_title="JARVIS AI Assistant",
        page_icon="🤖",
        layout="centered"
    )
    
    # Set custom styling
    set_custom_style()

    # Main content
    st.title("JARVIS AI Assistant")
    st.markdown("---")

    # Circular mic button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn = st.button(
            "🎙️" if not st.session_state.mic_active else "🔴",
            key="mic_button",
            help="Click to start/stop listening"
        )

    # Toggle state on button click
    if btn:
        st.session_state.mic_active = not st.session_state.mic_active
        st.rerun()

    # Add active state styling
    if st.session_state.mic_active:
        st.markdown(
            """
            <script>
            document.querySelector('.stButton button').classList.add('mic-active');
            </script>
            """,
            unsafe_allow_html=True
        )

    # Status indicator
    status_text = "🎤 Listening..." if st.session_state.mic_active else "🌟 Ready"
    sub_text = "Speak now!" if st.session_state.mic_active else "Click the microphone to start"
    
    st.markdown(
        f"""
        <div class="status-box">
            <h3>{status_text}</h3>
            <p>{sub_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()