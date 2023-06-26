import streamlit as st
import xml.etree.ElementTree as ET
import json
from pathlib import Path
import io
import os
import openai
from llama_index import GPTVectorStoreIndex, ServiceContext
from llama_index.query_engine import RetrieverQueryEngine
from langchain import OpenAI
from llama_index import download_loader
import os
from pathlib import Path

# from llama_index import download_loader

# # Initialize JSONReader
# JSONReader = download_loader("JSONReader")
# loader = JSONReader()




# Initialize JSONReader
JSONReader = download_loader("JSONReader")
loader = JSONReader()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_data(documents):
    # Load documents
    # documents = loader.load_data(json_file_path)
    
    # Initialize predictor
    llm_predictor = LLMPredictor(llm=OpenAI(temperature=0.15, model_name="text-davinci-003", max_tokens=1000))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)
    
    # Create vector index if not in session state
    if "vector_index" not in st.session_state:
        vector_index = GPTVectorStoreIndex.from_documents(documents, service_context=service_context)
        vector_retriever = vector_index.as_retriever(retriever_mode='embedding')
        vector_index = RetrieverQueryEngine(vector_retriever)
        st.session_state.vector_index = vector_index

    return st.session_state.vector_index, st.session_state

def xml_to_json(xml_str):
    """Function to convert XML to JSON"""
    data = ET.parse(io.StringIO(xml_str))
    root = data.getroot()

    def _parse(node):
        json_node = dict()
        if len(list(node)) == 0:
            return node.text
        else:
            for child in node:
                if child.tag not in json_node:
                    json_node[child.tag] = _parse(child)
                else:
                    if type(json_node[child.tag]) is list:
                        json_node[child.tag].append(_parse(child))
                    else:
                        json_node[child.tag] = [json_node[child.tag], _parse(child)]
        return json_node

    return _parse(root)

def app():
    """Main function that contains Streamlit code"""
    st.title('XML to JSON converter')
    
    uploaded_file = st.file_uploader('Upload XML file', type='xml')

    if uploaded_file is not None:
        try:
            bytes_data = uploaded_file.read()  # read as bytes
            str_data = bytes_data.decode("utf-8")  # convert to string
            json_data = xml_to_json(str_data)
            st.json(json_data)
            # Define json file path
            json_file_path = Path('./data.json')
            # Save json data to a file
            with json_file_path.open('w') as f:
                json.dump(json_data, f)
            # Load the data using the provided loader
            documents = loader.load_data(json_file_path)
            st.session_state.vector_index = process_data(documents)
            st.success("Vector Index created successfully")
        except Exception as e:
            st.write("Error occurred:", str(e))

    query = st.text_input("Enter query prompt")
    submit = st.button("Submit")

    if submit:
        vector_resp = st.session_state.vector_index.query(query).response
        st.write("### Vector Index Response:")
        st.write(vector_resp)


        #     st.write(documents)
        # except Exception as e:
        #     st.write("Error occurred:", str(e))

if __name__ == "__main__":
    app()
