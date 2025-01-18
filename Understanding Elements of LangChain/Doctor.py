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
st.title("DOCTOR CHATBOT 🩺")

# Input Query
query_text = st.text_input("What query would you like to ask?", "")

# Add a Submit button
if st.button("Submit"):
    if query_text:
        try:
            # Show a random fun fact while processing
            with st.spinner('Processing your query...'):
                # Show fun fact during processing
                random_fact = random.choice(fun_facts)
                st.info(f"Here's an interesting fact: {random_fact}")

                # Pass the input through the chain
                chain = prompt | llm | output_parser
                result = chain.invoke({"query": query_text})
                st.success(f"Response: {result}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a query before submitting.")