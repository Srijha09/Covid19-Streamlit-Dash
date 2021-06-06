import pandas as pd
import numpy as np
import streamlit as st
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
from sklearn.metrics import mean_squared_error
from fbprophet import Prophet


def load_data():
    """ Function to load data
        param DATA_URL: data_url
        return: pandas dataframe
    """
    DATA_URL = 'data/covid.csv'
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data

def forecast_global(df, feature):
    """ Function to forecast covid cases for the next one year
        param: dataframe(df) and dataframe attribute(feature)
        return forecast dataframe
    """
    data = df.groupby('Date').sum()[feature].reset_index()
    data.columns = ['ds','y']
    data['ds'] = pd.to_datetime(data['ds'])
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=365)
    #print(future.tail(5))
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    fig = m.plot(forecast)
    return fig

def forecast_global_components(df, feature):
    """ Function to forecast covid cases for the next one year
        param: dataframe(df) and dataframe attribute(feature)
        return forecast dataframe
    """
    data = df.groupby('Date').sum()[feature].reset_index()
    data.columns = ['ds','y']
    data['ds'] = pd.to_datetime(data['ds'])
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=365)
    #print(future.tail(5))
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    fig2 = m.plot_components(forecast)
    return fig2

def get_error_metrics(df,feature):
    data = df.groupby('Date').sum()[feature].reset_index()
    data.columns = ['ds','y']
    data['ds'] = pd.to_datetime(data['ds'])
    m = Prophet()
    m.fit(data)
    future = m.make_future_dataframe(periods=365)
    #print(future.tail(5))
    forecast = m.predict(future)
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
    return np.sqrt(mean_squared_error(data['y'],forecast['yhat'].head(data.shape[0])))


def main():
    df = load_data()
    st.title('Forecasting Covid 19 Cases using Prophet')
    graph_type = st.sidebar.selectbox("Choose what forecast you would like to view", ["Global"])
    if graph_type=='Global':
        view_type = st.selectbox("Choose what forecast you would like to view", ["Confirmed","Deaths",
                                                        "Recovered","Active"])
        if view_type=='Confirmed':
            st.subheader('Forecasting Confirmed Cases Worldwide(Baseline)')
            fig = forecast_global(df, feature='Confirmed')
            st.write(fig)
            fig1 = forecast_global_components(df, feature='Confirmed')
            st.write(fig1)
            rmse = get_error_metrics(df, feature='Confirmed')
            st.write('The root mean squared error is: ', rmse)
            st.write('This graph is taken in the form of A*10^8, where A is the number in the y-axis. This graph shows an upward trend. The confirmed cases seemed to have slowed down due to the roll out and the effectiveness of the vaccine. Hope to see a downward trend in the far future')

        if view_type=='Deaths':
            st.subheader('Forecasting Deaths Worldwide(Baseline)')
            fig = forecast_global(df, feature='Deaths')
            st.write(fig)
            fig1 = forecast_global_components(df, feature='Deaths')
            st.write(fig1)
            rmse = get_error_metrics(df, feature='Deaths')
            st.write('The root mean squared error is: ', rmse)
            st.write('There has been an overwhelming amount of deaths over the past one year. The number of deaths have slowed down but unfortunately, there were vast cases of death in India')
        
        if view_type=='Recovered':
            st.subheader('Forecasting Recovered Cases Worldwide(Baseline)')
            fig = forecast_global(df, feature='Recovered')
            st.write(fig)
            fig1 = forecast_global_components(df, feature='Recovered')
            st.write(fig1)
            rmse = get_error_metrics(df, feature='Recovered')
            st.write('The root mean squared error is: ', rmse)
            st.write('This graph kinda gives me the hope that things are going to get better with the amount of people who have recovered.')
        
        if view_type=='Active':
            st.subheader('Forecasting Active Cases Worldwide(Baseline)')
            fig = forecast_global(df, feature='Active')
            st.write(fig)
            fig1 = forecast_global_components(df, feature='Active')
            st.write(fig1)
            rmse = get_error_metrics(df, feature='Active')
            st.write('The root mean squared error is: ', rmse)
    

if __name__=='__main__':
    main()
