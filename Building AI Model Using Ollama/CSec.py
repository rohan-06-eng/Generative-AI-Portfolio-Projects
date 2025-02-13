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

# Output Parser
output_parser = StrOutputParser()

# Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an expert in cybersecurity, ethical hacking, and digital forensics. Provide up-to-date, detailed security advice and solutions based on the latest cybersecurity threats and vulnerabilities."),
        ("user", "Query: {query}")
    ]
)

# Ollama Model (Using Llama 3.2)
llm = Ollama(model="llama3.2")

# Cybersecurity Facts
cyber_facts = [
    "Did you know? The first computer virus, Creeper, was created in 1971 as an experimental program.",
    "Fun Fact: Over 90% of cyberattacks start with phishing emails.",
    "Here’s something interesting: The average cost of a data breach in 2023 was $4.45 million.",
    "Did you know? Multi-factor authentication (MFA) can prevent 99% of automated cyberattacks!",
    "Fun Fact: The longest known password in a data breach had 1,279 characters!",
    "Cyber Tip: Regularly updating your software and using strong, unique passwords can prevent most cyberattacks."
]

# Streamlit App
st.set_page_config(page_title="CyberSec Advisor 🔐", page_icon="🔒", layout="centered")

# Custom styling
st.markdown("""
    <style>
    body {
        background-color: #1e1e2e;
        color: white;
    }
    .stButton > button {
        background-color: #5a5a8e;
        color: white;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #3a3a6e;
    }
    h1 {
        color: #f8c291;
        text-align: center;
    }
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #5a5a8e;
        padding: 10px;
        font-size: 16px;
    }
    .stTextInput input:focus {
        border-color: #3a3a6e;
    }
    .stMarkdown {
        text-align: center;
    }
    .user-message {
        background-color: white;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    .expert-message {
        background-color: white;
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with Icon
st.markdown("<h1>CyberSec Advisor 🔐</h1>", unsafe_allow_html=True)

# Initialize conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

if 'query_text' not in st.session_state:
    st.session_state.query_text = ""

# Display conversation history
if st.session_state.conversation:
    st.write("### Conversation History:")
    for message in st.session_state.conversation:
        if message.startswith("You:"):
            st.markdown(f"<div class='user-message'>{message}</div>", unsafe_allow_html=True)
        elif message.startswith("CyberSec Expert:"):
            st.markdown(f"<div class='expert-message'>{message}</div>", unsafe_allow_html=True)

# Input Query
query_text = st.text_input("Ask your cybersecurity question:", value=st.session_state.query_text)

# Tooltip
st.info("Get expert cybersecurity advice. Type 'stop' to end the conversation.")

# Buttons
col1, col2 = st.columns([1, 1])
with col1:
    submit_button = st.button("Submit")
with col2:
    stop_button = st.button("Stop Conversation")

# Action for Submit button
if submit_button:
    if query_text.lower() == "stop":
        st.session_state.conversation.append("The conversation has ended.")
        st.write("Thank you for chatting with the CyberSec Expert!")
    elif query_text:
        # Show a random cybersecurity fact while processing
        with st.spinner('Analyzing your query...'):
            random_fact = random.choice(cyber_facts)
            st.info(f"Cybersecurity Fact: {random_fact}")

            # Pass query through the chain
            chain = prompt | llm | output_parser
            result = chain.invoke({"query": query_text})
            st.success(f"CyberSec Expert's Response: {result}")

            # Store the conversation
            st.session_state.conversation.append(f"You: {query_text}")
            st.session_state.conversation.append(f"CyberSec Expert: {result}")

        # Clear input
        st.session_state.query_text = ""

# Action for Stop button
if stop_button:
    st.session_state.conversation.append("The conversation has ended.")
    st.write("Thank you for chatting with the CyberSec Expert!")