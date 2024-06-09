import streamlit as st
import json
import os
from io import StringIO
import openai
from openai import OpenAI
from collections import defaultdict
from nltk import FreqDist
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
import nltk
nltk.download('stopwords')

st.set_page_config(page_title="BioMed Influencers Analysis", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
st.title("BioMed Influencers Analyis")

influencer_data = None

uploaded_file = st.file_uploader(
    "Upload a json file",
    type=["json"]
)
if uploaded_file is not None:
    influencer_data = StringIO(uploaded_file.getvalue().decode("utf-8"))
    string_data = influencer_data.read()

    openai.api_key = "sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G"
    client = OpenAI(
        # This is the default and can be omitted
        api_key="sk-proj-GE4QnuqouxONkJ8S7626T3BlbkFJA7d1AGUMAU8Q9TqwZl8G",
    )
    output = client.chat.completions.create(
        messages=[
            {
            "role": "user",
            "content": f"Act as an advisor who will help me to choose if the telegram channel is suitable for advertising. I need to decide if telegram channel is suitable for the advertising of a toothpaste product with an innovative whitening solution aimed at young people is placed. Input format is json with fields Text: stands for text of posts in channel, Views: stands for number of views on each post, Reposts: stands for number of reposts of post, Reactions: stands for number of reactions on post. Give a reason for influencer why his channel is suitable for advertisement or not suitable. Influence considered suitable if his posts in json field text contains themes about innovation, education, youth, health, self-care, it is also good if influencer have a large number of subscribers, reactions on posts. Я хочу видеть ответ на русском языке. Here is input data: {str(string_data)}. Напиши вывод в таком формате: Подходит или Неподходит. Причина: (Напиши подробную причину с аналитикой, фактами, цифрами, конкретными постами из которых ты сделал этот вывод, бери информацию только из input data, из представленного словаря с полями text, views, reactions, reposts. распиши причины для постов, реакций. Выведи id постов и их содержание на основе которых ты сделал вывод.",
        }
        ],
            model="gpt-3.5-turbo",
        )
    result = output.choices[0].message.content

    # Такие подходят
    st.info(result)
    st.title("BioMed Топ слов ВК")
    st.image('data/top_words_biomed_vk.png')
    
    st.title("BioMed Облако слов")
    st.image('data/word_cloud_biomed_vk.png')
    
    st.title("Инфлюенсер Облако слов")
    querywords = string_data.split(', ')
    resultwords  = [word for word in querywords if word.lower() not in stopwords.words('english') and word.lower() not in stopwords.words('russian')]
    result = ' '.join(resultwords)
    result = result.replace('null', '')
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110).generate(result)
    plt.figure(figsize=(10, 8))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(f'data/{uploaded_file.name}_word_cloud.png')
    st.image(f'data/{uploaded_file.name}_word_cloud.png')
    
