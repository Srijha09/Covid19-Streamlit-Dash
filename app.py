import streamlit as st 
import pandas as pd 
import numpy as np 
import pydeck as pdk 
import altair as alt 
from datetime import datetime
import pages.home
import pages.world
import pages.countrywise

PAGES = {
    "Home": pages.home ,
    "Worldwide" : pages.world,
    "Countrywise": pages.countrywise
}

def main():
    menu = st.sidebar.title("Menu")
    choice = st.sidebar.radio("Navigate", list(PAGES.keys()))
    PAGES[choice].main()
    st.sidebar.markdown(''' 
    This web application provides a holistic analysis of covid 19 cases around the world.
    Select the different options to vary the visualization.
    All the Charts are interactive. 

    Designed by: 
    **Srijha Kalyan**  ''')  

if __name__ == "__main__":
    main()

