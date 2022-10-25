import streamlit as st
import json
import pandas as pd
from urllib.request import urlopen
import altair as alt
import numpy as np


st.sidebar.header("Input parameters")
st.sidebar.write("This is the project sidebar \nIn here you can select different parameters that will affect all the visualizations in the page.")

#st.sidebar.subheader("Year selector")

#year = st.sidebar.slider("Year", 1960, 2020, 2020, step = 1)



st.sidebar.subheader("Region selector")


container = st.sidebar.container()
#container = st.sidebar.container()
#container = st.sidebar.container()


all = st.sidebar.checkbox("Select all")

if all:
    country = container.multiselect("Select the countries:",
        st.session_state['countries'], st.session_state['countries'])
else:
    country =  container.multiselect("Select the countries:",
        st.session_state['countries'])

st.markdown("""
            # Overview on Cereal Yield

            This is a dashboard that shows the quantity of cereal that has been yield for each country, for several years.
            In the dataframe you can see the raw data, while in the plot below you can the XXXXXXXX
        """)
    
df = st.session_state['cereal_output']
df = df[(df['country'].isin(country))]
df = df[df.columns[:-1]]
df = df.fillna(0)

st.dataframe(data= df)

df = df.transpose()
df = df.astype(int)

chart_data = pd.DataFrame(
    df,
    columns=df.columns)

st.line_chart(chart_data)#, height=500)

