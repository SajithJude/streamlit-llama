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

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize


openai.api_key = os.getenv("OPENAI_API_KEY")

def execute_query(prompt, course_name, directory):
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are generating a voiceover script for an e-learning course. The script should be formatted as separate sentences, with each sentence corresponding to a specific bullet point."},
        {"role": "user", "content": prompt}
      ]
    )
    
    # Assuming the generated voiceover script is the text returned
    return response.choices[0].message['content'].strip(), "Success"

def generate_voiceover_script(subtopic_name, bullets, course_name, directory):
    bullet_str = ' '.join(bullets)
    paragraph = f"{subtopic_name}. {bullet_str}"
    st.write("#### Paragraph")
    st.write(paragraph)

    vo_query = f"Please create a voice over script for the following points under the subtopic '{subtopic_name}': {bullet_str}. Each sentence of the script should correspond to one of the bullet points."
    vo_response, message = execute_query(vo_query, course_name, directory)
    vo_response = vo_response.replace("\n", "").replace("\\", "").replace("\"", "")
    return vo_response



def saveSubTopicBulletsWithVO(topics, course_settings, course_name, directory):
    for index, topic in enumerate(topics):
        subtopics = topic.get("subtopics", [])

        for sub_index, subtopic in enumerate(subtopics):
            bullets = subtopic.get("subtopic_bullets", [])
            bullet_texts = [bullet['bullet'] for bullet in bullets]
            subtopic_name = subtopic.get("subtopic_name", "")
            vo_script = generate_voiceover_script(subtopic_name, bullet_texts, course_name, directory)

            # Split the voiceover script into sentences
            vo_sentences = sent_tokenize(vo_script)
            
            # Check if the number of sentences matches the number of bullets
            if len(vo_sentences) == len(bullets):
                for bullet, sentence in zip(bullets, vo_sentences):
                    bullet["bullet_voiceover"] = sentence
            else:
                # In case the number of sentences doesn't match,
                # add the entire voiceover script to each bullet
                for bullet in bullets:
                    bullet["bullet_voiceover"] = vo_script
            
        # NoOfWordsForVOPerTopic = course_settings.get("NoOfWordsForVOPerTopic", 0)
        # Topicvoiceover_query = f"Generate voiceover for {topic_name} in {NoOfWordsForVOPerTopic} words"
        # Topicvoiceover, message = execute_query(Topicvoiceover_query, course_name, directory)
        # topic["topic_voiceover"] = Topicvoiceover.replace("\n","")

    return topics

# Streamlit app

st.title('Voiceover Script Generator')

json_input = st.text_area('Input JSON:')
but = st.button("submit")
if but:
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
    for topic in result['topics']:
        for subtopic in topic['subtopics']:
            st.markdown(f"**{subtopic['subtopic_name']}**")

            # Start a two-column layout
            col1, col2 = st.columns(2)

            # Bullets in the left column
            with col1:
                for bullet in subtopic['subtopic_bullets']:
                    st.write(bullet['bullet'])

            # Voiceover script in the right column
            with col2:
                for bullet in subtopic['subtopic_bullets']:
                    st.write(bullet['bullet_voiceover'])

            # End the two-column layout
