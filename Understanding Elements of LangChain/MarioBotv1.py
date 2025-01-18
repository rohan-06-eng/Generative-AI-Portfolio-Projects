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
        ("system", "You are Mario from Super Mario Bros. Answer as Mario, the assistant, only."),
        ("user", "Query: {query}")
    ]
)

# Ollama Model (Using Llama 3.2)
llm = Ollama(model="llama3.2")

# Streamlit App
st.title("MARIO CHATBOT 🍄")

# Input Query
query_text = st.text_input("What query would you like to ask?", "")

# Add a Submit button
if st.button("Submit"):
    if query_text:
        try:
            # Pass the input through the chain
            chain = prompt | llm | output_parser
            result = chain.invoke({"query": query_text})
            st.success(f"Response: {result}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query before submitting.")