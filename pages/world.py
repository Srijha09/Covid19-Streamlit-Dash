import os
import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime

def load_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = r'C:\Users\Srijhak\Documents\Covid19-Streamlit-Dash\data\covid.csv'
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data

@st.cache
def plot_snapshot_numbers(df, colors, country=None):
    """
    Function plots snapshots for worldwide and countries.
    :param df: DataFrame
    :param colors: list
    :param date: datetime object
    :param country: str
    :return: plotly.figure
    """
    with st.spinner("Rendering chart..."):
        colors = px.colors.qualitative.D3
        if country:
            df = df[df["Country/Region"] == country]
        fig = go.Figure()
        fig.add_trace(go.Bar(y=df[["Confirmed", "Deaths", "Recovered", "Active"]].columns.tolist(),
                             x=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                             text=df[["Confirmed", "Deaths", "Recovered", "Active"]].sum().values,
                             orientation='h',
                             marker=dict(color=[colors[1], colors[3], colors[2], colors[0]]),
                             ),
                      )
        fig.update_traces(opacity=0.7,
                          textposition=["inside", "outside", "inside", "inside"],
                          texttemplate='%{text:.3s}',
                          hovertemplate='Status: %{y} <br>Count: %{x:,.2f}',
                          marker_line_color='rgb(255, 255, 255)',
                          marker_line_width=2.5
                          )
        fig.update_layout(
            title="Total count",
            width=800,
            legend_title_text="Status",
            xaxis=dict(title="Count"),
            yaxis=dict(showgrid=False, showticklabels=True),
        )

    return fig

@st.cache
def plot_top_countries(df, colors):
    """
    Function plots top countries by confirmed, deaths, recovered, active cases.
    :param df: DataFrame
    :param colors: list
    :return: plotly.figure
    """
    with st.spinner("Rendering chart..."):
        temp = df.groupby("Country/Region").agg({"Confirmed": "sum",
                                                 "Deaths": "sum",
                                                 "Recovered": "sum",
                                                 "Active": "sum"})
        colors = px.colors.qualitative.Prism
        fig = make_subplots(2, 2, subplot_titles=("Top 10 Countries by cases",
                                                  "Top 10 Countries by deaths",
                                                  "Top 10 Countries by recoveries",
                                                  "Top 10 Countries by active cases"))
        fig.append_trace(go.Bar(x=temp["Confirmed"].nlargest(n=10),
                                y=temp["Confirmed"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=1)

        fig.append_trace(go.Bar(x=temp["Deaths"].nlargest(n=10),
                                y=temp["Deaths"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=2, col=1)

        fig.append_trace(go.Bar(x=temp["Recovered"].nlargest(n=10),
                                y=temp["Recovered"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=2)

        fig.append_trace(go.Bar(x=temp["Active"].nlargest(n=10),
                                y=temp["Active"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}'),
                         row=2, col=2)
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(
            opacity=0.7,
            marker_line_color='rgb(255, 255, 255)',
            marker_line_width=2.5
        )
        fig.update_layout(height=700,
                          width=1000,
                          showlegend=False)

    return fig



# show data on streamlit
def main():
    st.title("Worldwide Visualization of the Covid-19 Cases")
    df = load_data()
    st.write("The dataset was taken from [John Hopkins Covid19 data](https://github.com/CSSEGISandData/COVID-19)")

    graph_type = st.sidebar.selectbox("Choose a type of visualization", ["Map",
                                                        "Total Count",
                                                        "Comparison of countries"])

    #worldmap visualization of covid cases
    if (graph_type=="Map"):

        #total number of cases indicator
        fig = go.Figure()
        fig.add_trace(go.Indicator(mode="number",value=int(df['Confirmed'].sum()),number={"valueformat":"0.f","font":{"size":28}},
             title={"text":"Total_Confirmed","font":{"size":25}},domain={"row":0,"column":0}))

        fig.add_trace(go.Indicator(mode="number",value=int(df['Deaths'].sum()),number={"valueformat":"0.f","font":{"size":28}},
             title={"text":"Total_Deaths","font":{"size":25}},domain={"row":0,"column":1}))

        fig.add_trace(go.Indicator(mode="number",value=int(df['Recovered'].sum()),number={"valueformat":"0.f","font":{"size":28}},
             title={"text":"Total_Recovered","font":{"size":25}},domain={"row":1,"column":0}))

        fig.add_trace(go.Indicator(mode="number",value=int(df['Active'].sum()),number={"valueformat":"0.f","font":{"size":28}},
             title={"text":"Total_Active_Case","font":{"size":25}},domain={"row":1,"column":1}))

        fig.update_layout(grid={"rows":2,"columns":2})
        st.plotly_chart(fig)
       
        fig = px.choropleth(df,                        # Input Dataframe
                     locations="iso_code",           # identify country code column
                     color="Confirmed",                 # identify representing column
                     hover_name="Country/Region",        # identify hover name
                     animation_frame="Date",        # identify date column
                     projection="natural earth",        # select projection
                     color_continuous_scale = 'blues',  # select prefer color scale
                     range_color=[0,max(df['Confirmed']+2)]              # select range of dataset
                     )
        fig.update_layout(title="Use the slider to observe the rate of increase of the Covid 19 confirmed cases",height=500, width=800)
        st.plotly_chart(fig)

        
        

        fig1 = px.scatter_geo(df, locations="Country/Region", locationmode='country names', 
                     color="Deaths", size= df['Deaths'].pow(0.3), hover_name="Country/Region", 
                     range_color= [0, max(df['Deaths'])], 
                     projection="natural earth", animation_frame="Date", 
                     title='Progression of the number of deaths due to COVID-19')
        fig1.update_layout(height=550, width=850)
        
        st.plotly_chart(fig1)


    
    if(graph_type=="Total Count"):
        #barplot to show the changes in the covid 19 cases
        st.subheader('Changes in the covid cases over the world')
        fig = plot_snapshot_numbers(df, px.colors.qualitative.D3)
        st.plotly_chart(fig)

        st.subheader('Current active cases')
        datewise=df.groupby(["Date"]).agg({"Active":'sum'})
        fig=px.bar(x=datewise.index,y=datewise["Active"])
        fig.update_layout(title="Distribution of Number of Active Cases",
                  xaxis_title="Date",yaxis_title="Number of Cases",)
        st.plotly_chart(fig)

    if(graph_type=="Comparison of countries"):
        st.subheader('Top 10 countries with the highest Covid 19 cases')
        fig = plot_top_countries(df, px.colors.qualitative.D3)
        st.plotly_chart(fig)

        st.subheader('Timeline Comparision of covid 19 growth rate for various countries')
        country_name_input = st.multiselect('Select Country Names', df.groupby('Country/Region').count().reset_index()['Country/Region'].tolist())
        subset_data = df
        if len(country_name_input) > 0:
            subset_data = df[df['Country/Region'].isin(country_name_input)]
    
        fig = alt.Chart(subset_data).transform_filter(
        alt.datum.Confirmed > 0  
        ).mark_line().encode(
        x=alt.X('yearquarter(Date)', type='nominal', title='Date'),
        y=alt.Y('sum(Confirmed):Q',  title='Confirmed cases'),
        color='Country/Region',
        tooltip = 'sum(Confirmed)',
        ).properties(
        width=850,
        height=500
        ).configure_axis(
        labelFontSize=17,
        titleFontSize=20
        )
        
        st.altair_chart(fig)


if __name__=='__main__':
    main()





