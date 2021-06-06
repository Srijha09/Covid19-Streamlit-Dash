import pandas as pd
import numpy as np
import datetime
import pycountry 

def get_country_code(name):
    """
    Function  that produces ISO code for each country
    """
    try:
        return pycountry.countries.lookup(name).alpha_3
    except:
        None


def fetchdata():
    """
    Function that reads raw data from JHU timeseries dataset and performs preprocessing
    arg: None
    return: None
    """
    df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
    df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    df_recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')

    df_confirmed = df_confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Confirmed')
    df_deaths = df_deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Deaths')
    df_recovered = df_recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'], var_name='Date', value_name='Recovered')

    df_all =  df_confirmed.merge(right=df_deaths, how='left',on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])
    df_all = df_all.merge(right=df_recovered, how='left',on=['Province/State', 'Country/Region', 'Date', 'Lat', 'Long'])

    df_all['Confirmed'] = df_all['Confirmed'].fillna(0)
    df_all['Deaths'] = df_all['Deaths'].fillna(0)
    df_all['Recovered'] = df_all['Recovered'].fillna(0)
    df_all['Date'] = df_all['Date'].apply(lambda s: pd.to_datetime(s))
    df_all['iso_code'] = df_all['Country/Region'].apply(get_country_code)

    #tabulating the active cases
    df_all['Active'] = df_all['Confirmed'] - df_all['Deaths'] - df_all['Recovered']

    df_all.to_csv('data/covid.csv')

fetchdata()
