import streamlit as st
from dataframe_processing import Dataset
import datetime
st.set_page_config(layout="wide")

elec = Dataset('data.csv')
elec.load()

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

form_visual = st.form(key="my_form_visual", clear_on_submit=True)

with form_visual:
    submit_see = st.form_submit_button(label="Print")

if submit_see:
    st.write(elec.df)