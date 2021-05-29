import pandas as pd
import numpy as np
import datetime
import pycountry

def get_vacc_data():
    vaccine_data = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/vaccinations.csv')
    vaccine_loc = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/locations.csv')
    df_vaccine = pd.merge(vaccine_data, vaccine_loc, on=["location", "iso_code"])
    df_vaccine.drop(['daily_vaccinations_raw'], axis=1)
    df_vaccine['date'] = pd.to_datetime(df_vaccine['date'])
    df_vaccine = df_vaccine.sort_values('date', ascending=True)
    df_vaccine['date'] = df_vaccine['date'].dt.strftime('%Y-%m-%d')
    df_vaccine = df_vaccine.rename(columns={'location': 'country'})
    for iso_code in df_vaccine['iso_code'].unique():
        df_vaccine.loc[df_vaccine['iso_code'] == iso_code, :] = df_vaccine.loc[df_vaccine['iso_code'] == iso_code, :].fillna(method='ffill').fillna(0)
    df_vaccine.to_csv('data/df_vaccine.csv')

def aggregate(df: pd.Series, agg_col: str) -> pd.DataFrame:
    data = df.groupby(["country"])[agg_col].max()
    data = pd.DataFrame(data)
    return data

def get_summ_data():
    summary_data = pd.read_csv(r'C:\Users\Srijhak\Documents\Covid19-dash\data\worldometer_coronavirus_summary_data.csv')
    df_vaccine = pd.read_csv(r'C:\Users\Srijhak\Documents\Covid19-dash\data\df_vaccine.csv')
    df_vaccine.country = df_vaccine.country.replace().replace({
    "Antigua and Barbuda": "Antigua And Barbuda",
    "Bosnia and Herzegovina": "Bosnia And Herzegovina",
    "Brunei": "Brunei Darussalam",
    "Cape Verde": "Cabo Verde",
    "Cote d'Ivoire": "Cote D Ivoire",
    "Czechia": "Czech Republic", 
    "Democratic Republic of Congo": "Democratic Republic Of The Congo",
    "Falkland Islands": "Falkland Islands Malvinas",
    "Guinea-Bissau": "Guinea Bissau",
    "Isle of Man": "Isle Of Man",
    "North Macedonia": "Macedonia",
    "Northern Cyprus": "Cyprus",
    "Northern Ireland": "Ireland",
    "Saint Kitts and Nevis": "Saint Kitts And Nevis",
    "Saint Vincent and the Grenadines": "Saint Vincent And The Grenadines",
    "Sao Tome and Principe": "Sao Tome And Principe",
    "Sint Maarten (Dutch part)": "Sint Maarten",
    "Timor": "Timor Leste",
    "Trinidad and Tobago": "Trinidad And Tobago",
    "Turks and Caicos Islands": "Turks And Caicos Islands",
    "United Kingdom": "UK",
    "United States": "USA",
    "Vietnam": "Viet Nam",
    "Wallis and Futuna": "Wallis And Futuna Islands"})

    df_vaccine = df_vaccine[df_vaccine.country.apply(lambda x: x not in ['Bonaire Sint Eustatius and Saba','England','Eswatini','Guernsey','Hong Kong','Jersey','Kosovo','Macao',
'Nauru','Palestine','Pitcairn','Scotland','Tonga','Turkmenistan','Tuvalu', 'Wales'])]

    summary = summary_data.set_index("country")
    vaccines = df_vaccine[['country', 'vaccines']].drop_duplicates().set_index('country')
    summary = summary.join(vaccines)
    for cols in df_vaccine.columns[4:-4]:
        summary = summary.join(aggregate(df_vaccine,cols))
    summary['vaccinated_percent'] = summary.total_vaccinations / summary.population * 100
    summary['tested_positive'] = summary.total_confirmed / summary.total_tests * 100
    summary.to_csv('data/summary_df.csv')

def get_daily_data():
    df_daily = pd.read_csv(r'C:\Users\Srijhak\Documents\Covid19-dash\data\worldometer_coronavirus_daily_data.csv')
    df_vaccine = pd.read_csv(r'C:\Users\Srijhak\Documents\Covid19-dash\data\df_vaccine.csv')
    # use only common countries and dates 
    countries = df_vaccine.dropna(subset=['daily_vaccinations'])['country'].unique()
    dates = df_vaccine.dropna(subset=['daily_vaccinations'])['date'].unique()
    country_mask = df_daily.country.apply(lambda x: x in countries)
    date_mask = df_daily.date.apply(lambda x: x in dates)

    # generate the visualization data 
    columns_to_sum = ['daily_new_cases', 'cumulative_total_cases', 'cumulative_total_deaths', 'active_cases']
    daily_cases = df_daily[country_mask & date_mask].groupby('date')[columns_to_sum].sum()
    daily_vaccs = df_vaccine.groupby('date')[[ 'daily_vaccinations']].sum()

    # make it a dataframe for convenience  
    data = pd.DataFrame(daily_cases).join(pd.DataFrame(daily_vaccs))

    # bring back the vaccine data we prepared in the previous section 
    cumulative_vaccines = pd.DataFrame(df_vaccine.groupby('date')['total_vaccinations'].sum())
    data = data.join(cumulative_vaccines).reset_index()
    data.to_csv('data/df_daily.csv')

get_vacc_data()
get_daily_data()
get_summ_data()