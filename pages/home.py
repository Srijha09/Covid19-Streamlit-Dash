import streamlit as st
from PIL import Image

def main():
    image = Image.open("assets/world.png")
    st.image(image)
    st.title("Welcome to the COVID-19 Dashboard")
    st.write("""
    This dashboard will be able to analyze, visualize, the spread of the novel Coronavirus - 2019 (COVID - 19)
    caused by severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). Additionally, it provides an analysis of the vaccinations that have started rolling out by the end of 2020.
    """)
    st.markdown("## Symptoms")
    st.markdown(("* Fever or chills\n* Cough\n"
                "* Shortness of breath or difficulty breathing\n"
                "* Fatigue\n"
                "* Muscle or body aches\n"
                "* Headache\n"
                "* Loss of taste or smell\n"
                "* Sore throat\n"
                "* Congestion or runny nose\n"
                "* Nausea or vomiting\n"
                "* Diarrhea"))
    st.markdown("## Resources")
    st.markdown(("* [World Health Organization](https://www.who.int/maternal_child_adolescent/links/covid19-resources-and-support-for-mncah-and-ageing/en/)\n"
                 "* [Center for Disease Control](https://www.cdc.gov/coronavirus/2019-ncov/index.html)\n"
                 "* [National Institute of Health](https://www.nih.gov/coronavirus)"))