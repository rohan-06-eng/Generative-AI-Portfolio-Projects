import os
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set environment variables
os.environ['LANGCHAIN_API_KEY'] = os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_PROJECT'] = os.getenv('LANGCHAIN_PROJECT')

# Environment Setup
import streamlit as st
from langchain_community.llms import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Output Parser (should be defined before using)
output_parser = StrOutputParser()

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an experienced, compassionate psychiatrist with deep knowledge of mental health practices, able to provide insightful, evidence-based advice and explanations in a kind and empathetic manner."),
        ("user", "Query: {query}")
    ]
)

# Ollama Model (Using Llama 3.2)
llm = Ollama(model="llama3.2")

# Mental Health Tips (instead of fun facts)
mental_health_tips = [
    "Remember: It's okay to not be okay. Talk to someone when you feel overwhelmed.",
    "Self-care isn't selfish. It's necessary for your well-being.",
    "Sometimes the bravest thing you can do is ask for help.",
    "Breathing exercises can help you calm your mind and body. Try taking deep breaths.",
    "Your mental health is just as important as your physical health."
]

# Streamlit App
st.set_page_config(page_title="Digital Therapist Bot: Your Emotional Support 💙🌿", page_icon="🧠", layout="centered")

# Custom styling (soothing colors and a calm aesthetic)
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #d1c4e9, #b39ddb);  /* Soothing purple gradient background */
    }
    .stButton > button {
        background-color: #9575cd;  /* Soft purple button color */
        color: white;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #7e57c2;  /* Darker purple for hover effect */
    }
    h1 {
        color: #4a148c;  /* Deep purple for header */
        text-align: center;
    }
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #9575cd;
        padding: 10px;
        font-size: 16px;
    }
    .stTextInput input:focus {
        border-color: #7e57c2;
    }
    .stSpinner {
        color: #9575cd;  /* Matching spinner color with the theme */
    }
    .stAlert {
        background-color: #ffcccb;  /* Soft red alert background */
    }
    .stMarkdown {
        text-align: center;
    }
    /* User Message Styling */
    .user-message {
        background-color: #d0f0c0;  /* Light green background for user messages */
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    /* Doctor Message Styling */
    .doctor-message {
        background-color: #cce7ff;  /* Light blue background for doctor responses */
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with Icon and Text
st.markdown("<h1 style='text-align: center;'>Digital Therapist Bot: Your Emotional Support 💙🌿</h1>", unsafe_allow_html=True)

# Initialize a session state for conversation tracking
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Initialize session state for user input (keeps the input text when submitting)
if 'query_text' not in st.session_state:
    st.session_state.query_text = ""

# Display conversation history with color-coded messages
if st.session_state.conversation:
    st.write("### Conversation History:")
    for message in st.session_state.conversation:
        if message.startswith("You:"):
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
        elif message.startswith("Psychiatrist:"):
            st.markdown(f"<div class='doctor-message'>{message}</div>", unsafe_allow_html=True)

# Input Query
query_text = st.text_input("What would you like to ask the psychiatrist?", value=st.session_state.query_text)

# Add an informative tooltip for the user input
st.info("Ask your mental health-related questions. Type 'stop' to end the conversation.")

# Add Submit and Stop buttons in the same line using columns
col1, col2 = st.columns([1, 1])
with col1:
    submit_button = st.button("Submit")
with col2:
    stop_button = st.button("Stop Conversation")

# Action for Submit button
if submit_button:
    if query_text.lower() == "stop":
        st.session_state.conversation.append("The conversation has ended.")
        st.write("Thank you for chatting with the Digital Therapist Bot!")
    elif query_text:
        # Show a random mental health tip while processing
        with st.spinner('Processing your query...'):
            random_tip = random.choice(mental_health_tips)
            st.info(f"Here's a helpful tip: {random_tip}")

            # Pass the input through the chain and get the psychiatrist's response
            chain = prompt | llm | output_parser
            result = chain.invoke({"query": query_text})
            st.success(f"Psychiatrist's Response: {result}")

            # Store the user query and psychiatrist's response in the conversation history
            st.session_state.conversation.append(f"You: {query_text}")
            st.session_state.conversation.append(f"Psychiatrist: {result}")

        # Clear the input box after submission
        st.session_state.query_text = ""  # Clear input after submission

# Action for Stop button
if stop_button:
    st.session_state.conversation.append("The conversation has ended.")
    st.write("Thank you for chatting with the Digital Therapist Bot!")
