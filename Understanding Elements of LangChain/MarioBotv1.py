import os
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
        ("system", "You are Mario from Super Mario Bros. Answer as Mario, the assistant, only. Use a cheerful and playful tone!"),
        ("user", "Query: {query}")
    ]
)

# Ollama Model (Using Llama 3.2)
llm = Ollama(model="llama3.2")

# Streamlit App
st.title("MARIO CHATBOT 🍄")

# Background Color (Mario Inspired, Softened)
st.markdown("""
    <style>
    .stApp {
        background-color: #f8e5a6;  /* Soft Mario Yellow */
    }
    .stTextInput input {
        background-color: #f2a7a0;  /* Soft Mario Red */
        color: black;
    }
    .stButton>button {
        background-color: #4b90d4; /* Soft Mario Blue */
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Input Query
query_text = st.text_input("What query would you like to ask?", "")

# Add a Submit button with Mario's playful character
if st.button("Let's Go! 🚀"):
    if query_text:
        try:
            # Display loading spinner while processing the query
            with st.spinner('Wahoo! Mario is thinking...'):
                # Pass the input through the chain
                chain = prompt | llm | output_parser
                result = chain.invoke({"query": query_text})
                st.success(f"Here you go! 🎮: {result}")
        except Exception as e:
            st.error(f"Oh no! Something went wrong: {e}")
    else:
        st.warning("Mama mia! You need to ask a question first.")