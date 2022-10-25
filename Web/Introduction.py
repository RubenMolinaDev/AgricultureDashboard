import streamlit as st
from streamlit_multipage import MultiPage

import json
import pandas as pd
from urllib.request import urlopen
import altair as alt
import numpy as np

st.set_page_config(
    page_title="Introduction",
)

# 1. HACEMOS RETRIEVE DE LOS DATOS DE SUPERFICIE AGROLOGICA

@st.cache
def Getting_pct_agricultural_land_surface():
    # Primero necesitamos el dataframe, haciendo un request a nuestro servidor

    url_backend = 'http://127.0.0.1:8005/'
    # store the response of URL
    response = urlopen(url_backend + "agriculture/surface_percentage")

    data_json = json.loads(response.read())
    all_info = pd.read_json(data_json) # In this point we have a Pandas dataset of name and region.
    all_info["country"] = all_info.index
    all_info = pd.melt( all_info, id_vars = 'country', value_vars = all_info.columns[:-1])
    all_info.columns = ['Country', 'Year', 'Percentage of agricultural land']
    return all_info#.transpose()

@st.cache
def Getting_irr_agricultural_land_surface():
    # Primero necesitamos el dataframe, haciendo un request a nuestro servidor

    url_backend = 'http://127.0.0.1:8005/'
    # store the response of URL
    response = urlopen(url_backend + "agriculture/surface_irrigation")

    data_json = json.loads(response.read())
    all_info = pd.read_json(data_json) # In this point we have a Pandas dataset of name and region.
    all_info["country"] = all_info.index
    all_info = all_info.dropna(how='all', axis=1)
    all_info = all_info.dropna(how='all', axis=0)
    all_info = pd.melt( all_info, id_vars = 'country', value_vars = all_info.columns[:-1])
    all_info.columns = ['Country', 'Year', 'Percentage of irrigated agricultural land']

    return all_info#.transpose()

@st.cache
def Merging_data(df1, df2):
    df = df1.merge(df2, left_on=['Country', 'Year'], right_on=['Country', 'Year'])
    return df

@st.cache
def Getting_cereal_production():
    # Primero necesitamos el dataframe, haciendo un request a nuestro servidor

    url_backend = 'http://127.0.0.1:8005/'
    # store the response of URL
    response = urlopen(url_backend + "cereal/yield")

    data_json = json.loads(response.read())
    all_info = pd.read_json(data_json) # In this point we have a Pandas dataset of name and region.
    all_info["country"] = all_info.index
    #all_info = pd.melt( all_info, id_vars = 'country', value_vars = all_info.columns[:-1])
    #all_info.columns = ['Country', 'Year', 'Cereal production (metric tons)']
    return all_info#.transpose()


# LOAD THE SESSIONS

if not 'irr_surface' in st.session_state.keys():
    irr_surface = Getting_irr_agricultural_land_surface()
    st.session_state['irr_surface'] = irr_surface

if not 'pct_surface' in st.session_state.keys():
    pct_surface = Getting_pct_agricultural_land_surface()
    st.session_state['pct_surface'] = pct_surface

if not 'merged_df' in st.session_state.keys():
    merged_df = Merging_data(irr_surface, pct_surface)
    st.session_state['merged_df'] = merged_df

if not 'cereal_output' in st.session_state.keys():
    cereal_output = Getting_cereal_production()
    st.session_state['cereal_output'] = cereal_output

if not 'countries' in st.session_state.keys():
    countries = ['AFG','ARE','ARG','ARM','AUS','AUT','AZE','BEL','BEN','BGD','ZWE', 'ZMB', 'YEM', 'PSE']
    st.session_state['countries'] = countries


st.write("# Welcome to Ruben's BASF Challenge!")

st.sidebar.success("To start select a dashboard above.")

st.markdown(
    """
    This is a dashboard made for a general overview on Agriculture 
    and Cereal yield data based on World Open Bank Data.

    ### About the frontend? 
    - Made with [streamlit.io](https://streamlit.io)
    ### The backend is made with FastAPI

"""
)