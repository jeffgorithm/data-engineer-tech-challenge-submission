import streamlit as st
import pandas as pd

def read_json(file_path):
    df = pd.read_json(path_or_buf=file_path)

    return df

if __name__ == '__main__':
    df = read_json('covid_cases.json')

    st.bar_chart(data=df['Cases'])
    st.line_chart(data=df['Cases'])
    st.area_chart(data=df['Cases'])
    