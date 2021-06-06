# Covid19-Streamlit-Dash

This Covid19 Dashboard provides are holistic analysis of the cases of the virus around the world and countrywise. It also provides a vaccination analysis administered worldwide.

The following tasks have been done to create this application
- **TASK 1** : Performed data preprocessing and EDA to prepare dataset for proper analysis. Automatic data fetch from JHU dataset on github
- **TASK 2** : Data visualization of the worldwide cases was carried out using plotly and altair : Confirmed, Recovered, Deaths. Additionally compared the top 10 countries with Covid 19 cases
- **TASK 3** : Data visualization country-wise and province/state-wise was also done using plotly. Additionally a time series comparison was performed for various countries
- **TASK 4** : Time Series Forecasting using Prophet was performed for predicting global cases
- **TASK 5** : Vaccination Analysis was performed for worldwide, country-wise and vaccine-type wise. Inference from the analysis was noted
- **TASK 6** : Deployed the Streamlit App in Heroku Cloud


## How to run
Clone the repository and install dependencies:

```shell script
pip3 install -r requirements.txt
```

Run the app using streamlit

```shell script
streamlit run app.py
```

## References
https://towardsdatascience.com/covid-19-data-processing-58aaa3663f6

https://github.com/Sayar1106/covid-dashboard

https://www.kaggle.com/pawanbhandarkar/covid-19-eda-man-vs-disease

https://facebook.github.io/prophet/
