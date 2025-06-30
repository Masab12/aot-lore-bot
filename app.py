# Main Application file created by Masab Farooque
# This is the user interface for our Attack on Titan LoreBot.

import streamlit as st
from PIL import Image
import base64
from core.aot_rag_brain import create_the_rumbling_chain

# --- Page Configuration ---
# Using the Scout Regiment icon for our app
icon = Image.open("assets/icon.png")
st.set_page_config(
    page_title="Shingeki no Kyojin: LoreBot",
    page_icon=icon,
    layout="centered"
)

# --- Asset Loading ---
# Function to load and encode images and CSS to inject into the app
def load_and_encode_asset(file_path):
    with open(file_path, "rb") as f:
        data = base64.b64encode(f.read()).decode("utf-8")
    return data

# Encode our assets
background_image_encoded = load_and_encode_asset("assets/background.jpg")
custom_css_encoded = load_and_encode_asset("assets/style.css")

# --- UI Styling ---
# Injecting our custom CSS for that super appealing look
st.markdown(
    f"""
    <style>
    {custom_css_encoded}
    
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{background_image_encoded}");
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# --- Session State Initialization ---
# This is where we keep our variables safe across app reruns, like memories.
if 'eren_yeager_chain' not in st.session_state:
    with st.spinner("Initializing the Coordinate... The Founder is waking up..."):
        # This is our main RAG chain, let's call him Eren Yeager
        st.session_state.eren_yeager_chain = create_the_rumbling_chain()

if 'chat_history' not in st.session_state:
    # This will store our conversation history
    st.session_state.chat_history = []


# --- Main App Interface ---
st.title("🔰 Shingeki no Kyojin: LoreBot 🔰")
st.markdown("<p>Created with dedication by Masab Farooque</p>", unsafe_allow_html=True)


# --- Chat Interface ---
# Display previous messages from history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Get new user input
user_prompt_from_paradise = st.chat_input("Ask about the world of Attack on Titan...")

if user_prompt_from_paradise:
    # Add user message to history and display it
    st.session_state.chat_history.append({"role": "user", "content": user_prompt_from_paradise})
    with st.chat_message("user"):
        st.markdown(user_prompt_from_paradise)

    # The bot's turn to think and respond
    with st.spinner("The Survey Corps is gathering intelligence... Please wait..."):
        # Calling our RAG chain (Eren!) to get a response
        response_from_the_founder = st.session_state.eren_yeager_chain.invoke(
            {"question": user_prompt_from_paradise}
        )
        
        bot_response = response_from_the_founder["answer"]
        
        # This is a small fallback logic, like a last resort
        if "I don't know" in bot_response or "I cannot answer" in bot_response:
            bot_response = "My knowledge is limited to my archives. I can't seem to find information on that. Perhaps try asking about Titans, Eldia, or the Rumbling?"

    # Display the bot's response
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Add bot's response to history
    st.session_state.chat_history.append({"role": "assistant", "content": bot_response})