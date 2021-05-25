import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime


#loading the data
def load_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = r'C:\Users\Srijhak\Documents\Covid19-dash\data\covid.csv'
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
        colors = px.colors.qualitative.Set1
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

@st.cache(suppress_st_warning=True)
def plot_top_states(df, country=None):
    """
    Function plots top provinces by confirmed, deaths, recovered, active cases.
    :param df: DataFrame
    :param colors: list
    :return: plotly.figure
    """
    with st.spinner("Rendering chart..."):
        df = df[df["Country/Region"] == country]
        if df["Province/State"].isnull().all():
            st.info("Sorry we do not have province/state level information for {}".format(country))

        else:
        
            df = df.groupby(["Province/State"]).agg({"Confirmed": "sum",
                                             "Deaths": "sum",
                                             "Recovered": "sum",
                                             "Active": "sum"})
            colors = px.colors.qualitative.Prism
            fig = make_subplots(2, 2, subplot_titles=("Top 10 Province/States by cases",
                                                  "Top 10 Province/States by deaths",
                                                  "Top 10 Province/States by recoveries",
                                                  "Top 10 Province/States by active cases"))
            fig.append_trace(go.Bar(x=df["Confirmed"].nlargest(n=10),
                                y=df["Confirmed"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=1)

            fig.append_trace(go.Bar(x=df["Deaths"].nlargest(n=10),
                                y=df["Deaths"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=2, col=1)

            fig.append_trace(go.Bar(x=df["Recovered"].nlargest(n=10),
                                y=df["Recovered"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}',
                                ),
                         row=1, col=2)

            fig.append_trace(go.Bar(x=df["Active"].nlargest(n=10),
                                y=df["Active"].nlargest(n=10).index,
                                orientation='h',
                                marker=dict(color=colors),
                                hovertemplate='<br>Count: %{x:,.2f}'),
                         row=2, col=2)
            fig.update_yaxes(autorange="reversed")
            fig.update_traces(
            opacity=0.7,
            marker_line_color='rgb(255, 255, 255)',
            marker_line_width=2.5)
            fig.update_layout(height=700,
                          width=1000,
                          showlegend=False)

            return fig



def timeline(df, feature, country=None):
    """
    Function plots  time series charts for worldwide as well as countries
    :param df: DataFrame
    :param color: list
    :param country: str
    :return: plotly.figure, DataFrame
    """
    with st.spinner("Rendering chart..."):
        color = px.colors.qualitative.Set1
        if country:
            df = df[df['Country/Region'] == country]
        
        temp = df.groupby(['Date']).agg({feature: "sum"}).reset_index()
        
        fig = go.Figure()
        fig.add_trace(go.Line(
            x=temp['Date'],
            y=temp[feature],
            marker=dict(color=color[2]),
            hovertemplate='Date: %{x} <br>Count: %{y:,.2f}',
        ))
        
        return fig

def main():
    st.title("Visualization of the Covid-19 Cases Countrywise")
    df = load_data()
    country = st.sidebar.selectbox("Select country",df["Country/Region"].unique())
    #barplot to show the changes in the covid 19 cases

    graph_type = st.sidebar.selectbox("Choose visualization", ["Total Count",
                                                        "Timeline","Province/States"])
    if(graph_type=="Total Count"):
        st.header(f'Changes in the covid cases in {country}')
        fig = plot_snapshot_numbers(df, px.colors.qualitative.D3, country)
        st.plotly_chart(fig)
    
    if(graph_type=="Timeline"):
        st.header(f'Timeline of the covid cases in {country}')
        feature = st.selectbox("Select one", ['Confirmed', 'Deaths','Recovered'])
        fig = timeline(df,feature,country=country)
        st.plotly_chart(fig)
    
    if(graph_type=="Province/States"):
        st.header(f'Top 10 Province/States with highest covid cases in {country}')
        fig = plot_top_states(df,country=country)
        st.plotly_chart(fig)


if __name__=='__main__':
    main()
    
     
