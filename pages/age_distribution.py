import streamlit as st
import altair as alt
import os
import json
import pandas as pd
import streamlit as st

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
chart = alt.Chart(source).mark_bar().encode(
    x=alt.X('age', title='Возраст', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('count():Q', title='Кол-во респондентов', axis=alt.Axis(tickMinStep=1)),
    tooltip='count()'
).interactive()
st.altair_chart(chart, use_container_width=True)
