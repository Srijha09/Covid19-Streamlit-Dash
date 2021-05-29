from PIL import Image
from _plotly_utils.colors import colorscale_to_colors
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime


def load_vaccine_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = r'C:\Users\Srijhak\Documents\Covid19-dash\data\df_vaccine.csv'
    data = pd.read_csv(DATA_URL)
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    return data

def load_daily_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = r'C:\Users\Srijhak\Documents\Covid19-dash\data\df_daily.csv'
    data = pd.read_csv(DATA_URL)
    data['date'] = pd.to_datetime(data['date']).dt.strftime('%Y-%m-%d')
    return data

def load_summary_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = r'C:\Users\Srijhak\Documents\Covid19-dash\data\summary_df.csv'
    data = pd.read_csv(DATA_URL)
    return data

def get_multiline_title(title:str, subtitle:str):
    return f"{title}<br><sub>{subtitle}</sub>"

def bar_plot(df,xcol, ycol,title,color, n=None):
    with st.spinner("Rendering chart..."):
        df = df.sort_values(ycol, ascending=False).dropna(subset=[ycol]) 
        if  n is not None:
            df = df.iloc[:n]
        else:
            n = " "
        fig = go.Figure(go.Bar(
                     hoverinfo='skip',
                     x=df[xcol], 
                     y=df[ycol], 
                     marker=dict(
                     color = df[ycol],
                     colorscale = color,
                        ),
                    ),
                )
    
        fig.update_layout(
            height=700, 
            width = 1000,
            title=title,
            xaxis_title=f"Top Countries",
            yaxis_title="Count/Percent",
            plot_bgcolor='rgba(0,0,0,0)',
        )
    
        return fig


        
def main():
    st.title("Covid 19 Vaccination Analysis")
    image = Image.open("assets/vacc.png")
    st.image(image)
    st.write("The vaccinations had started rolling out during the end of 2020. The dataset starts from the beginning of January 2021. The vaccination dataset has been taken from [Our World in Data](https://github.com/owid/covid-19-data/tree/master/public) and the world cases summary data has been scraped from [Worldometer.info](https://www.worldometers.info/coronavirus/about/). This dashboard provides a holistic view of the vaccination administered in various parts of the world. This analysis will be able to provide us insights of Covid 19 Vaccine.")
    graph_type = st.selectbox("Choose visualization", ["Worldwide",
                                                        "Manufacture-wise"])
    vacc_df = load_vaccine_data()
    summ_df = load_summary_data()
    daily_df = load_daily_data()
    if graph_type=='Worldwide':
        fig = px.choropleth(vacc_df,                        # Input Dataframe
                     locations="iso_code",           # identify country code column
                     color="total_vaccinations",                 # identify representing column
                     hover_name="country",        # identify hover name
                     animation_frame="date",        # identify date column
                     projection="natural earth",        # select projection
                     color_continuous_scale ='viridis',  # select prefer color scale
                     range_color=[0,50000000]              # select range of dataset
                     )
        fig.update_layout(title="Use the slider to observe the vaccination progress in various countries",height=500, width=800)
        st.plotly_chart(fig)
        st.write("It is clear that most of the developed countries have started receiving high dosages of vaccine. Whereas, there are undeveloped countries in Africa that are yet to receive the vaccine. The grey colours on the world map indicate that data has not been given for these places.")

    
        #barplot of top 20 countries
        title = get_multiline_title("Top 20 countries vaccination", "Countries with individuals who have received the first dose of the vaccine")
        fig = bar_plot(summ_df.reset_index(),'country',"total_vaccinations", title,"Reds", n=20)
        st.plotly_chart(fig)
        st.write("Its noticable that China and USA are leading in the highest vaccinations administered for the first dose.")

        title = get_multiline_title("Top 30 countries vaccination per hundred", "Countries with individuals who have received the first dose of the vaccine")
        fig = bar_plot(summ_df.reset_index(),'country',"total_vaccinations_per_hundred", title, "turbid", n=30)
        st.plotly_chart(fig)

        title = get_multiline_title("Top 30 countries with poeple fully vaccination per hundred", "Countries with individuals who have received the both the dose of the vaccine")
        fig = bar_plot(summ_df.reset_index(),'country',"people_fully_vaccinated_per_hundred", title, "Blugrn", n=30)
        st.plotly_chart(fig)

        #barplot for vaccine percentage
        title = get_multiline_title("Top 30 countries vaccination percentage", "Countries with individuals who have received the first dose of the vaccine")
        fig = bar_plot(summ_df.reset_index(),'country',"vaccinated_percent", title, "purples", n=30)
        st.plotly_chart(fig)

        title = get_multiline_title("Top 30 countries with daily vaccinations", "Countries with individuals who have received the first dose of the vaccine")
        fig = bar_plot(summ_df.reset_index(),'country',"daily_vaccinations", title, "blues", n=30)
        st.plotly_chart(fig)

        title = get_multiline_title("Comparing the growth of Vaccine vs Virus", "Comparing the total number of daily new cases and daily vaccinations globally")
        fig = go.Figure(data=[
                go.Bar(
                    name="New Cases",
                    x=daily_df['date'], 
                    y=daily_df['daily_new_cases'],
                    marker_color="MediumPurple",
                ),
                go.Bar(
                    name="Vaccinated",
                    x=daily_df['date'], 
                    y=daily_df['daily_vaccinations'],
                    marker_color="LightSkyBlue"
                ),

            ])

        fig.update_layout(
        title=title,
        xaxis_title="Date",
        yaxis_title="Count",
        height = 500,
        width = 800,
        plot_bgcolor='rgba(0,0,0,0)',
        barmode='stack',
        hovermode="x"
        )

        st.plotly_chart(fig)

    
    if graph_type=="Manufacture-wise":
        data = summ_df.reset_index().dropna(subset=['vaccines'])
        #worldmap for popular vaccines
        fig = px.choropleth(data, locations="country", 
                    locationmode='country names',
                    color="vaccines", 
                    hover_name="country", 
                   )
        fig.update_layout(title="Popular Vaccines used Worldwide", title_x=0.5, legend_orientation = 'h', height=500, width=900)
        st.plotly_chart(fig)

        #barplot for popular vaccines
        title = get_multiline_title("Types of Vaccinations in Use", "Vaccinations based on the manufacturer in preference.")
        fig = bar_plot(data.reset_index(),'vaccines',"total_vaccinations", title, "turbid", n=30)
        st.plotly_chart(fig)
        st.write("We can see that the Chinese vaccine (Sinopharm) has been most frequently used. Most of the countries are using Pfizer and Moderna")



if __name__=='__main__':
    main()
