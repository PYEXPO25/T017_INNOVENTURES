import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

# Streamlit UI
st.set_page_config(page_title="AI Chatbot", layout="centered")

st.title("💬 LLM-Based Chatbot")
# st.write("Ask me anything!")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! 😊 I'm your AI assistant. How can I help you today?"}
    ]

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_input = st.chat_input("What's on your mind?")

if user_input:
    # Append user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Display user input in chat
    with st.chat_message("user"):
        st.markdown(user_input)

    # Create prompt for Groq's LLaMA model
    prompt_template = f"""
    You are an AI chatbot. Answer any question clearly and concisely.

    ### Chat History:
    {st.session_state.messages}

    ### User's Message:
    {user_input}
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