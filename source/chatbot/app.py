import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from langdetect import detect

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", layout="centered")

st.title("💬 Multilingual LLM-Based Chatbot")
st.write("Ask me anything! (Supports English & Tamil)")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! I can answer your questions in English & Tamil. How can I assist you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Detect the language of user input
    detected_lang = detect(user_input)
    if detected_lang not in ["en", "ta","arabic"]:
        detected_lang = "en"  # Default to English for unsupported languages

    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user input in chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create prompt for Groq's LLaMA model with multilingual support
    prompt_template = f"""
    You are an AI chatbot that supports English and Tamil. 
    - If the user types in arabic, respond in Tamil. 
    - If the user types in English, respond in English.
    - Keep responses clear and concise.

    ### Chat History:
    {st.session_state.messages}

    ### User's Message:
    {user_input}

    ### Language Detected:
    {detected_lang}
    """

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):
            try:
                completion = client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "system", "content": prompt_template}],
                    temperature=0.7,
                    max_tokens=2000,
                    top_p=1,
                    stream=False,
                )

                response_text = completion.choices[0].message.content.strip()
                st.markdown(response_text)

                # Append AI response to chat history
                st.session_state.messages.append({"role": "assistant", "content": response_text})

            except Exception as e:
                st.error(f"Error: {str(e)}")