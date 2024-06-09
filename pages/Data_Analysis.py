import streamlit as st
import altair as alt
import json
import os
import pandas as pd
import openai
from openai import OpenAI
from collections import defaultdict

st.set_page_config(page_title="BioMed Data Analysis", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("BioMed Data Analyis")

def build_dataframe():
    path = os.getcwd() + '/responces'
    all_responses = []

    for file in os.listdir(path):
        full_filename = "%s/%s" % (path, file)
        with open(full_filename,'r') as fi:
            if full_filename.endswith('.gitignore'): continue

            all_responses.append(json.load(fi))

    df = pd.DataFrame(all_responses)

    return df

st.title("Распределение количества ответов по возрастам")
source = build_dataframe().drop_duplicates(['userId', 'age'])
if not source.empty:
    chart = alt.Chart(source).mark_bar().encode(
        x=alt.X('age', title='Возраст', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('count():Q', title='Кол-во респондентов', axis=alt.Axis(tickMinStep=1)),
        tooltip='count()'
    ).interactive()
    st.altair_chart(chart, use_container_width=True)

# Путь к директории с JSON файлами
directory = 'responces'

# Список для хранения значений по ключу 'prompt'
prompts_list = []

# Перебор всех файлов в директории
for file in os.listdir(directory):
    # Проверка, является ли файл JSON файлом
    if file.endswith('.json'):
        # Открытие файла
        with open(os.path.join(directory, file), 'r') as f:
            # Чтение содержимого файла как JSON объекта
            data = json.load(f)
            # Добавление значения по ключу 'prompt' в список
            prompts_list.append(data['prompt'])

# Вывод списка значений по ключу 'prompt'
print(prompts_list)
print(len(prompts_list))

openai.api_key = "sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G"
client = OpenAI(
    # This is the default and can be omitted
    api_key="sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G",
)
keywords_dict = defaultdict(int)
for prompt in prompts_list:
    output = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Retrieve key-words from this string {prompt}. Output format is keyword, keyword, keyword",
            }
        ],
        model="gpt-3.5-turbo",
    )
    keywords_string = output.choices[0].message.content
    keywords_list = keywords_string.split(', ')
    print(keywords_list)
    for key in keywords_list:
        keywords_dict[key] += 1

st.title("Ключевые слова в вопросах пользователей")
keywords_dict = {k: v for k, v in sorted(keywords_dict.items(), reverse=True, key=lambda item: item[1])}
st.bar_chart(keywords_dict)

st.warning("В связи с часто встречающимися вопросами о принципе работы технологии отбеливания рекомендуем добавить в пост эту информацию.")
