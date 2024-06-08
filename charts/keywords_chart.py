import json
import os
import openai
import streamlit as st
from openai import OpenAI
from collections import defaultdict

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
print(keywords_dict)

words_and_counts = keywords_dict.items()
sorted_words_and_counts = sorted(words_and_counts, key=lambda x: (-x[1], x[0]))

st.bar_chart(sorted_words_and_counts, x="Частота встречаемости", y="Ключевое слово", color="col3")
