import streamlit as st
import pandas as pd
from datetime import date

def read_json(file_path):
    df = pd.read_json(path_or_buf=file_path)
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    df['Weekly Moving Average'] = df['Cases'].rolling(window=7).mean()
    df['Monthly Moving Average'] = df['Cases'].rolling(window=30).mean()

    return df

def filter_data(df, time_range):
    filter_df = df[(df['Date'] >= time_range[0]) & (df['Date'] <= time_range[1])]
    
    return filter_df, df

if __name__ == '__main__':
    df = read_json('covid_cases.json')

    st.title('No. of Covid-19 cases vs Time')

    time_range = st.slider(
        label="Select Date Range",
        value=(date(2020, 3, 1), date(2020, 9, 1)),
        format="DD/MM/YY",
        min_value=date(2020, 3, 1),
        max_value=date(2023, 3, 31)
        )

    filter_df, df = filter_data(df, time_range)

    st.bar_chart(data=filter_df, x='Date', y='Cases')
    st.line_chart(data=filter_df, x='Date', y=['Cases', 'Weekly Moving Average', 'Monthly Moving Average'])
        