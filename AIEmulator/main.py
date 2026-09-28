import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from database import get_langchain_db
import os

# Initialize OpenAI and validate API key
load_dotenv("secure.env", override=True)
print("API key found:", os.getenv("OPENAI_API_KEY") is not None)
if not (api_key := os.getenv("OPENAI_API_KEY")):
    st.error("Please set OPENAI_API_KEY in .env")
    st.stop()

# Setup LangChain components
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
# Initialize SQL agent with the database toolkit
agent = create_sql_agent(
    llm=llm,
    toolkit=SQLDatabaseToolkit(
        db=get_langchain_db(),
        llm=llm
    ),
    verbose=True,
    handle_parsing_errors=True
)

# Setup Streamlit UI
st.title("💬 Company Information Chatbot")
st.write("Ask questions about the company.")

# Initialize session state for storing results
if 'result' not in st.session_state:
    st.session_state.result = None

# Create input field first
user_input = st.text_input("Your question:", key="input_field")

# Place buttons below the input
col1, col2 = st.columns([1, 1])
ask_button = col1.button("Ask")
clear_button = col2.button("Clear")

# Create container for results
result_container = st.container()

# Handle user query
if ask_button and user_input.strip():
    with st.spinner("Thinking..."):
        try:
            st.session_state.result = agent.run(user_input)
        except Exception as e:
            st.session_state.result = f"Error: {e}"

# Display results in container
if st.session_state.result:
    with result_container:
        if "Error:" in str(st.session_state.result):
            st.error(st.session_state.result)
        else:
            st.success(st.session_state.result)

# Reset functionality
if clear_button:
    st.session_state.clear()
    st.rerun()