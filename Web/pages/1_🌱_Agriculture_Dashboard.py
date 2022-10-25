import streamlit as st
import json
import pandas as pd
from urllib.request import urlopen
import altair as alt
import numpy as np

st.sidebar.write("This is the project sidebar \nIn here you can select different parameters that will affect all the visualizations in the page.")

st.sidebar.subheader("Parameters:")

year = st.sidebar.slider("Year", 1960, 2020, 2020, step = 1)

container = st.sidebar.container()

all = st.sidebar.checkbox("Select all")

if all:
    country = container.multiselect("Select the countries:",
        st.session_state['countries'], st.session_state['countries'])
else:
    country =  container.multiselect("Select the countries:",
        st.session_state['countries'])

a1, a2 = st.columns(2)

a1.markdown("""
            ### Relationship between irrigated land and agricultural land.
            
            In this dashboard you can observe data regarding the agricultural land for different countries.

            - In the former plot you can find a representation on the percentage of irrigated land vs percentage of agricultural land

            - In the latter plot you can find the percentage of agricultural land dedicated for each country.
        
            """)

#a2.markdown("#### Relation between irrigated and agricultural land.")

pct_irr_surface_df = st.session_state['merged_df']
pct_irr_surface_df = pct_irr_surface_df[(pct_irr_surface_df['Year'] == 'YR' + str(year)) & \
                                        (pct_irr_surface_df['Country'].isin(country))]

if len(pct_irr_surface_df) == 0 or pct_irr_surface_df.isnull().values.all():
    
    a2.write("# ")
    a2.write("# ")
    a2.write("# ")
    a2.write("No data available with parameters selected .")

else:

    d = alt.Chart(pct_irr_surface_df ).mark_circle().encode(
            x = 'Percentage of agricultural land',
            y = 'Percentage of irrigated agricultural land',
            size=alt.Size('point_size:N', scale=None),
            #color = 'Size',
            tooltip = ['Country', 'Percentage of irrigated agricultural land', 'Percentage of agricultural land']
        ).interactive()

    a2.altair_chart(d, use_container_width=True)


pct_surface_df = st.session_state['pct_surface']
pct_surface_df = pct_surface_df[(pct_surface_df['Year'] == 'YR' + str(year)) & \
                                        (pct_surface_df['Country'].isin(country))]

st.markdown("#### Percentage of agricultural land in different countries.")

#st.dataframe(data=pct_surface_df)
st.bar_chart(data=pct_surface_df, x='Country', y=['Percentage of agricultural land'])


#st.bar_chart(data=st.session_state['pct_surface'] ,
#                x=None, 
#                y=None, 
#                width=0, 
#                height=0, 
#                use_container_width=True)


