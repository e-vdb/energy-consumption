import streamlit as st
from dataframe_processing import Dataset
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from graphic import setup_bar_chart


st.set_page_config(layout="wide")
list_years = [(datetime.today() + relativedelta(years=-i)).year for i in range(5)]
dataCointe = Dataset('data_Cointe.csv')
dataCointe.load()
cols = list(dataCointe.df.columns)

# Set the app title
st.title("Energy consumption")
st.write(
    "Save and visualise your energy consumption"
)
st.header('Fill your index')
form = st.form(key="my_form", clear_on_submit = True)
with form:
    d = st.date_input(
        "Date",
        value=pd.to_datetime("2021-12-01", format="%Y-%m-%d"))
    day_rec = st.number_input('Electricity index (day)')
    night_rec = st.number_input('Electricity index (night)')
    rec_gas = st.number_input('Gas index')
    rec_water = st.number_input('Water index')
    submit = st.form_submit_button(label="Add")

if submit:
    data = [d, day_rec, night_rec, rec_gas, rec_water]
    newline = {col: val for col, val in zip(cols, data)}
    dataCointe.add(newline)

st.header('Plot consumption')
form_visual = st.form(key="my_form_visual", clear_on_submit=True)
with form_visual:
    submit_see = st.form_submit_button(label="Print")
    option = st.selectbox(
        'Year',
        list_years)

if submit_see:
    elec_col = ['day_consumption (kWh)', 'night_consumption (kWh)']
    col = ['consumption (m3)']
    elec.consumption(elec_col[0], 'day_record')
    elec.consumption(elec_col[1], 'night_record')
    gas.consumption(col[0], 'record')
    water.consumption(col[0], 'record')
    for data in datasets:
        data.filter_year(str(option))
    st.subheader('Electricity')
    fig_elec = setup_bar_chart(elec.df, 'consumption_month', elec_col)
    fig_gas = setup_bar_chart(gas.df, 'consumption_month', col)
    fig_water = setup_bar_chart(water.df, 'consumption_month', col)
    st.plotly_chart(fig_elec, use_container_width=True)
    st.subheader('Gas')
    st.plotly_chart(fig_gas, use_container_width=True)
    st.subheader('Water')
    st.plotly_chart(fig_water, use_container_width=True)
