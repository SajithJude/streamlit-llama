# # Install necessary libraries
# # pip install llama_index html2text streamlit openai

# import os
# import openai
# import streamlit as st
# from llama_index import VectorStoreIndex, SimpleWebPageReader

# # openai.api_key = os.getenv("OPENAI_API_KEY")

# os.environ['OPENAI_API_KEY'] =  os.getenv("OPENAI_API_KEY")

# # Initialize chat engine
# def initialize_chat_engine(data):
#     index = VectorStoreIndex.from_documents(data)
#     chat_engine = index.as_chat_engine(chat_mode='react', verbose=True)
#     return chat_engine

# # Function for chat interaction
# def chat_interaction(chat_engine, question):
#     response = chat_engine.chat(question)
#     return response

# st.title("Interactive Quiz Bot")

# # The URL of the webpage you want to use as the knowledge base
# url = st.text_input("Enter the URL of the webpage you want to use as the knowledge base:")
# buto = st.button("submit")
# if buto:
#     data = SimpleWebPageReader(html_to_text=True).load_data([url])
#     chat_egine = initialize_chat_engine(data)

# st.subheader("Interactive Quiz")
# question = st.text_input("Enter your question:")
# if st.button("Submit"):
#     response = chat_interaction(chat_egine, question)
#     st.write(response)

