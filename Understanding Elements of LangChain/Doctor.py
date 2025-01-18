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
        ("system", "You are an experienced, educated doctor with in-depth knowledge of medical practices, able to provide accurate, evidence-based advice and explanations in a clear and concise manner."),
        ("user", "Query: {query}")
    ]
)

# Ollama Model (Using Llama 3.2)
llm = Ollama(model="llama3.2")

# Fun Facts
fun_facts = [
    "Did you know? The human body contains around 37.2 trillion cells.",
    "Fun Fact: The average adult body has around 5 liters of blood circulating.",
    "Here’s something interesting: Our stomach gets a new lining every 3 to 4 days.",
    "Did you know? A human sneeze can travel as fast as 100 miles per hour!",
    "Fun Fact: Your heart beats about 100,000 times per day!"
]

# Streamlit App
st.set_page_config(page_title="Doctor Chatbot 🩺", page_icon="🩺", layout="centered")

# Custom styling (soft colors and aesthetics)
st.markdown("""
    <style>
    body {
        background-color: #f0f8ff;  # Light blue background
    }
    .stButton > button {
        background-color: #68a0b0;  # Soft teal button color
        color: white;
        border-radius: 10px;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: bold;
    }
    .stButton > button:hover {
        background-color: #4d8a96;  # Darker teal for hover effect
    }
    h1 {
        color: #5e8c8e;  # Soft teal header color
        text-align: center;
    }
    .stTextInput input {
        border-radius: 10px;
        border: 2px solid #68a0b0;
        padding: 10px;
        font-size: 16px;
    }
    .stTextInput input:focus {
        border-color: #4d8a96;
    }
    .stSpinner {
        color: #68a0b0;  # Matching spinner color with the theme
    }
    .stAlert {
        background-color: #ffcccb;  # Soft red alert background
    }
    .stMarkdown {
        text-align: center;
    }
    /* User Message Styling */
    .user-message {
        background-color: #d0f0c0;  # Light green background for user messages
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    /* Doctor Message Styling */
    .doctor-message {
        background-color: #cce7ff;  # Light blue background for doctor responses
        padding: 8px;
        border-radius: 5px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Title with Icon and Text
st.markdown("<h1 style='text-align: center;'>Doctor Chatbot 🩺</h1>", unsafe_allow_html=True)

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
        elif message.startswith("Doctor:"):
            st.markdown(f"<div class='doctor-message'>{message}</div>", unsafe_allow_html=True)

# Input Query
query_text = st.text_input("What would you like to ask the doctor?", value=st.session_state.query_text)

# Add an informative tooltip for the user input
st.info("Ask your health-related questions. Type 'stop' to end the conversation.")

# Add a Submit button with the improved design
if st.button("Submit"):
    if query_text.lower() == "stop":
        st.session_state.conversation.append("The conversation has ended.")
        st.write("Thank you for chatting with the Doctor!")
    elif query_text:
        # Show a random fun fact while processing
        with st.spinner('Processing your query...'):
            random_fact = random.choice(fun_facts)
            st.info(f"Here's an interesting fact: {random_fact}")

            # Pass the input through the chain and get the doctor's response
            chain = prompt | llm | output_parser
            result = chain.invoke({"query": query_text})
            st.success(f"Doctor's Response: {result}")

            # Store the user query and doctor's response in the conversation history
            st.session_state.conversation.append(f"You: {query_text}")
            st.session_state.conversation.append(f"Doctor: {result}")

        # Save the current input text to session state so it remains visible
        st.session_state.query_text = ""  # Clear input after submission
