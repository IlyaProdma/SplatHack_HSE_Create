import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
import json
from datetime import datetime

st.set_page_config(page_title="BioMed Addvertisement Chat", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = "sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G"
st.title("BioMed Addvertisement Chat 💬🦙")
st.info("Загляни на [сайт BioMed](https://biomedglobal.net/?section=promo)", icon="📃")
st.image('posts/biomed_molecular.png', caption='BioMed MOLECULAR WHITE')
         
if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Задай любой вопрос про этот пост"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Загрузка и индексация данных BioMed. Это займет 1-2 минуты."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the BioMed products, and also health and care specialist, including teeth and your job is to answer questions in simple words. Assume that all questions are related to BioMed. Keep your answers simple and based on facts – do not hallucinate features."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
            timestamp = datetime.now().isoformat()
            data = {
                "prompt": str(prompt),
                "response": str(response.response),
                "timestamp": str(timestamp)
            }
            json_data = json.dumps(data, ensure_ascii=False)

            # Сохраняем данные в файл (предполагается, что файл questions_and_answers.json существует)
            with open(f'responces/{timestamp}.json', 'w') as file:
                file.write(json_data)
