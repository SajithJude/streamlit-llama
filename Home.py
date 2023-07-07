# import streamlit as st
# from llama_index import (
#     GPTVectorStoreIndex, Document, SimpleDirectoryReader,
#     QuestionAnswerPrompt, LLMPredictor, ServiceContext, TreeIndex
# )
# from llama_index.query_engine import RetrieverQueryEngine
# import openai
# from langchain import OpenAI
# from tempfile import NamedTemporaryFile
# from llama_index import download_loader
# import os
# from pathlib import Path
# PDFReader = download_loader("PDFReader")

# openai.api_key = os.getenv("OPENAI_API_KEY")

# def process_pdf(uploaded_file):
#     loader = PDFReader()
#     with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
#         temp_file.write(uploaded_file.getvalue())
#         documents = loader.load_data(file=Path(temp_file.name))
    
#     llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.15, model_name="text-davinci-003", max_tokens=1000))
#     service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    
#     if "vector_index" not in st.session_state:
#         vector_index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
#         vector_retriever = vector_index.as_retriever(retriever_mode='embedding')
#         vector_index = RetrieverQueryEngine(vector_retriever)
#         st.session_state.vector_index = vector_index

#     modes = ['root', 'all_leaf', 'select_leaf_embedding', 'select_leaf']
#     for mode in modes:
#         if f"tree_index_{mode}" not in st.session_state:
#             tree_index = TreeIndex.from_documents(documents, service_context=service_context)
#             tree_retriever = tree_index.as_retriever(retriever_mode=mode)
#             tree_index = RetrieverQueryEngine(tree_retriever)
#             st.session_state[f"tree_index_{mode}"] = tree_index
    
#     return st.session_state.vector_index, st.session_state

# uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

# if uploaded_file is not None:
#     if "vector_index" not in st.session_state:
#         st.session_state.vector_index, st.session_state = process_pdf(uploaded_file)
#         st.success("Vector Index and all Tree Indexes created successfully")

# query = st.text_input("Enter query prompt")
# asl = st.button("Submit")

# if asl:
#     vector_resp  = st.session_state.vector_index.query(query).response
#     st.write("### Vector Index Response:")
#     st.write(vector_resp)

#     modes = ['root', 'all_leaf', 'select_leaf_embedding', 'select_leaf']
#     for mode in modes:
#         tree_resp = st.session_state[f"tree_index_{mode}"].query(query).response
#         st.write(f"### Tree Index Response ({mode}):")
#         st.write(tree_resp)


# Install necessary libraries
# pip install llama_index html2text streamlit openai

import os
import openai
import streamlit as st
from llama_index import VectorStoreIndex, SimpleWebPageReader

# openai.api_key = os.getenv("OPENAI_API_KEY")

os.environ['OPENAI_API_KEY'] =  os.getenv("OPENAI_API_KEY")

# Initialize chat engine
def initialize_chat_engine(data):
    
# Function for chat interaction
def chat_interaction(chat_engine, question):
    response = chat_engine.chat(question)
    return response

st.title("Interactive Quiz Bot")

# The URL of the webpage you want to use as the knowledge base
url = st.text_input("Enter the URL of the webpage you want to use as the knowledge base:")
buto = st.button("submit")
if buto:
    data = SimpleWebPageReader(html_to_text=True).load_data([url])
    st.write(data)
    index = VectorStoreIndex.from_documents(data)
    chat_engine = index.as_chat_engine(chat_mode='react', verbose=True)
    # return chat_engine

    
    # chat_egine = initialize_chat_engine(data)
    st.write(chat_egine)

    # pass

st.subheader("Interactive Quiz")
question = st.text_input("Enter your question:")
if st.button("Submit"):
    response = chat_interaction(chat_egine, question)
    st.write(response)

