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
st.write('Electricity')
form = st.form(key="my_form", clear_on_submit = True)
with form:
    d = st.date_input(
        "Date",
        datetime.date(2021, 12, 7))
    day_rec = st.number_input('Day')
    night_rec = st.number_input('Night')
    submit = st.form_submit_button(label="Add")
if submit:
    df2 = {'date': d, 'day_record': day_rec, 'night_record': night_rec}
    elec.fill(df2)
    elec.save()

st.write('Gas')
form_gas = st.form(key="my_form_gas", clear_on_submit=True)
with form_gas:
    d = st.date_input(
        "Date",
        datetime.date(2021, 12, 7))
    rec_gas = st.number_input('record')
    submit_gas = st.form_submit_button(label="Add")
if submit_gas:
    df2 = {'date': d, 'record': rec_gas}
    gas.fill(df2)
    gas.save()

st.write('Water')
form_water = st.form(key="my_form_water", clear_on_submit=True)
with form_water:
    d = st.date_input(
        "Date",
        datetime.date(2021, 12, 7))
    rec_water = st.number_input('record')
    submit_water = st.form_submit_button(label="Add")
if submit_water:
    df2 = {'date': d, 'record': rec_water}
    water.fill(df2)
    water.save()

st.write('Show index')
form_visual = st.form(key="my_form_visual", clear_on_submit=True)

with form_visual:
    submit_see = st.form_submit_button(label="Print")

if submit_see:
    st.write(elec.df)
    st.write(gas.df)
    st.write(water.df)