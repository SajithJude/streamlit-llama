import streamlit as st
import json


import streamlit as st
from llama_index import (
    GPTVectorStoreIndex, Document, SimpleDirectoryReader,
    QuestionAnswerPrompt, LLMPredictor, ServiceContext
)
from llama_index.query_engine import RetrieverQueryEngine
import openai
from langchain import OpenAI
from tempfile import NamedTemporaryFile
from llama_index import download_loader
import os
from pathlib import Path
# PDFReader = download_loader("PDFReader")

openai.api_key = os.getenv("OPENAI_API_KEY")


def execute_query(prompt, course_name, directory):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "Generate a voice over script for the paragraphs beloning to the subtopics for an e-learning video"},
        {"role": "user", "content": prompt}
      ]
    )
    
    # Assuming the generated voiceover script is the text returned
    return response.choices[0].message['content'].strip(), "Success"
def generate_voiceover_script(subtopic_name, bullets, course_name, directory):
    paragraph = subtopic_name + '\n' + '\n'.join(bullets)
    vo_query = f"Generate a voice over script for the following paragraph of '{paragraph}'."
    vo_response, message = execute_query(vo_query, course_name, directory)
    vo_response = vo_response.replace("\n", "").replace("\\", "").replace("\"", "")
    return vo_response

def saveSubTopicBulletsWithVO(topics, course_settings, course_name, directory):
    for index, topic in enumerate(topics):
        subtopics = topic.get("subtopics", [])
        topic_name = topic.get("topic_name")

        for sub_index, subtopic in enumerate(subtopics):
            bullets = subtopic.get("subtopic_bullets", [])
            bullet_texts = [bullet['bullet'] for bullet in bullets]
            subtopic_name = subtopic.get("subtopic_name", "")
            vo_script = generate_voiceover_script(subtopic_name, bullet_texts, course_name, directory)
            
            for bullet in bullets:
                bullet["bullet_voiceover"] = vo_script

        NoOfWordsForVOPerTopic = course_settings.get("NoOfWordsForVOPerTopic", 0)
        Topicvoiceover_query = f"Generate voiceover for {topic_name} in {NoOfWordsForVOPerTopic} words"
        Topicvoiceover, message = execute_query(Topicvoiceover_query, course_name, directory)
        topic["topic_voiceover"] = Topicvoiceover.replace("\n","")

    return topics

# Streamlit app

st.title('Voiceover Script Generator')

json_input = st.text_area('Input JSON:')
if json_input:
    data = json.loads(json_input)

    # Extract the necessary information
    result = data["result"]
    course_name = result["course_name"]
    topics = result["topics"]
    course_settings = {}  # Replace with your actual course settings
    directory = ""  # Replace with your actual directory

    # Run your function
    new_topics = saveSubTopicBulletsWithVO(topics, course_settings, course_name, directory)

    # Replace the old topics with the new ones in the result
    result["topics"] = new_topics

    # Display the updated JSON
    st.json(result)
