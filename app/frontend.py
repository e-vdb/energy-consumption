import streamlit as st
from dataframe_processing import Dataset
import datetime
st.set_page_config(layout="wide")

elec = Dataset('data.csv')
gas = Dataset('data_gas.csv')
water = Dataset('data_water.csv')
datasets = [elec, gas, water]
for data in datasets:
    data.load()

# Set the app title
st.title("Energy consumption")
st.write(
    "Save and visualise your energy consumption"
)
st.write('Fill your index')
form = st.form(key="my_form", clear_on_submit = True)
with form:
    d = st.date_input(
        "Date",
        datetime.date(2021, 12, 7))
    day_rec = st.number_input('Electricity index (day)')
    night_rec = st.number_input('Electricity index (night)')
    rec_gas = st.number_input('Gas index')
    rec_water = st.number_input('Water index')
    submit = st.form_submit_button(label="Add")

if submit:
    df_elec = {'date': d, 'day_record': day_rec, 'night_record': night_rec}
    elec.fill(df_elec)
    elec.save()
    df_gas = {'date': d, 'record': rec_gas}
    gas.fill(df_gas)
    gas.save()
    df_water = {'date': d, 'record': rec_water}
    water.fill(df_water)
    water.save()

st.write('Show index')
form_visual = st.form(key="my_form_visual", clear_on_submit=True)
with form_visual:
    submit_see = st.form_submit_button(label="Print")

if submit_see:
    elec.consumption('day_consumption  (kWh)', 'day_record')
    elec.consumption('night_consumption (kWh)', 'night_record')
    gas.consumption('consumption (m3)', 'record')
    water.consumption('consumption (m3)', 'record')
    st.write(elec.df)
    st.write(gas.df)
    st.write(water.df)