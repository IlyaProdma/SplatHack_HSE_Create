import streamlit as st
import openai
from llama_index.llms.openai import OpenAI
try:
  from llama_index import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
except ImportError:
  from llama_index.core import VectorStoreIndex, ServiceContext, Document, SimpleDirectoryReader
import json
from datetime import datetime
import uuid
    
st.set_page_config(page_title="BioMed Advertisement Chat", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = "sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G"
st.title("BioMed Addvertisement Chat 💬🦙")
st.info("Загляни на [сайт BioMed](https://biomedglobal.net/?section=promo)", icon="📃")
IMAGE_PATH = "posts/biomed_molecular.png"
#st.image(IMAGE_PATH, caption='BioMed MOLECULAR WHITE')
POST_TEXT = '''
🌿✨ #BiomedBeats: Мы знаем, как важно найти моменты радости и покоя среди бешеного ритма жизни. 
В связи с этим хотим поделиться своим плейлистом, который поможет начать день с белоснежной улыбки.
Кроме того, скоро у нас выходит новая паста  - MOLECULAR WHITE, которая отлично справляется с отбеливанием зубов и на 99% безопаснее существующих аналогов 
за счет инновационной технологии очистки.

Мы подготовили для вас нечто особенное —  приглашаем создать свой собственный плейлист для чистки зубов и поделиться им с миром! 
Почему стоит участвовать?
Поделитесь своей музыкой: Найдите единомышленников и вдохновитесь плейлистами других.
Будьте на волне: Участвуйте в жизни сообщества Biomed, наслаждайтесь моментами и создавайте контент, который принесет радость другим.
Получите шанс на подарок: Лучшие плейлисты получат приятные сюрпризы от Biomed!
Присоединяйтесь к акции #BiomedBeats и превратите ежедневную рутину в момент радости и заботы о себе. 
Потому что даже самые простые вещи могут приносить счастье. 

Как принять участие?
Используйте наш хэштег #BiomedBeats, чтобы все могли найти и послушать ваши любимые треки для этих волшебных минут.

Плейлисты, которые нам больше всего откликнуться используем в следующем видео-рассказе MOLECULAR WHITE:)
'''
st.info(POST_TEXT)
# Job Age Sex (M F)
# Ключевые слова из вопросов

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Задай любой вопрос про этот пост"}
    ]

@st.cache_resource(show_spinner=False)
def load_data():
    with st.spinner(text="Загрузка и индексация данных BioMed. Это займет 1-2 минуты."):
        reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
        docs = reader.load_data()
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5, system_prompt="You are an expert on the BioMed products, and also health and care specialist, including teeth and your job is to answer questions in simple words. Assume that all questions are related to BioMed. Keep your answers simple and based on facts – do not hallucinate features. Отвечай только на русском языке."))
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        return index

index = load_data()

if "user" not in st.session_state.keys():
    st.session_state.user = {
       "user_id": uuid.uuid4(),
       "job": '',
       "sex": 'M',
       "age": ''
    }

if "form_submitted" not in st.session_state.keys():
    st.session_state.form_submitted = False

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
        st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])


# form to collect user data
if st.session_state.form_submitted == False:
    with st.form("used_data_form"):
        st.write("Заполните данные о себе")
    
        st.session_state.user['job'] = st.text_input("Род деятельности")
        st.session_state.user['age'] = st.number_input("Возраст", min_value=0, step=1, format="%d")
        st.session_state.user['sex'] = 'F' if st.toggle("Пол М/Ж") else 'M'
        
        # Every form must have a submit button.
        st.session_state.form_submitted = st.form_submit_button("Подтвердить")
        print(st.session_state.form_submitted)


# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(f"Use this information about post and answer questions: {POST_TEXT}. " + prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history
            timestamp = datetime.now().isoformat()
            data = {
                "userId": str(st.session_state.user['user_id']),
                "prompt": str(prompt),
                "response": str(response.response),
                "timestamp": str(timestamp),
                "job": str(st.session_state.user['job']),
                "age": str(st.session_state.user['age']),
                "sex": st.session_state.user['sex']
            }
            json_data = json.dumps(data, ensure_ascii=False)

            # Сохраняем данные в файл (предполагается, что файл questions_and_answers.json существует)
            with open(f'responces/{timestamp}.json', 'w') as file:
                file.write(json_data)
