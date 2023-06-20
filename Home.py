import streamlit as st
from llama_index import (
    GPTVectorStoreIndex, Document, SimpleDirectoryReader,
    QuestionAnswerPrompt, LLMPredictor, ServiceContext, TreeIndex,
    TreeRootRetriever
)
from llama_index.query_engine import RetrieverQueryEngine
import openai
from langchain import OpenAI
from tempfile import NamedTemporaryFile
from llama_index import download_loader
import os
from pathlib import Path
PDFReader = download_loader("PDFReader")

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_pdf(uploaded_file):
    loader = PDFReader()
    with NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
        temp_file.write(uploaded_file.getvalue())
        documents = loader.load_data(file=Path(temp_file.name))
    
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.15, model_name="text-davinci-003", max_tokens=1000))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    
    if "vector_index" not in st.session_state:
        vector_index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        vector_retriever = vector_index.as_retriever(retriever_mode='embedding')
        vector_index = RetrieverQueryEngine(vector_retriever)
        st.session_state.vector_index = vector_index

    if "tree_index" not in st.session_state:
        tree_index = TreeIndex.from_documents(documents, service_context=service_context)
        tree_retriever = TreeRootRetriever(tree_index)
        tree_index = RetrieverQueryEngine(tree_retriever)
        st.session_state.tree_index = tree_index
    
    return st.session_state.vector_index, st.session_state.tree_index

uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file is not None:
    if "vector_index" not in st.session_state or "tree_index" not in st.session_state:
        st.session_state.vector_index, st.session_state.tree_index = process_pdf(uploaded_file)
        st.success("Both Vector Index and Tree Index created successfully")

query = st.text_input("Enter query prompt")
asl = st.button("Submit")

if asl:
    vector_resp  = st.session_state.vector_index.query(query).response
    tree_resp = st.session_state.tree_index.query(query).response
    st.write("Vector Index Response:", vector_resp)
    st.write("Tree Index Response:", tree_resp)
