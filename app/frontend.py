import streamlit as st
from dataframe_processing import Dataset
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from graphic import setup_bar_chart
from data_processing import find_csv_filenames, create_dataset


st.set_page_config(layout="wide")
list_years = [(datetime.today() + relativedelta(years=-i)).year for i in range(5)]
dataCointe = Dataset('data_Cointe.csv')
dataCointe.load()

def load_file():
    filenames = find_csv_filenames("/home/emeline/PycharmProjects/energy-consumption")
    file = st.selectbox(
        'Files',
        filenames)
    return file

# Set the app title
st.title("Energy consumption")
st.write(
    "Save and visualise your energy consumption"
)

expander = st.expander('Create a new record')
with expander:
    form_create = st.form(key="my_form_create", clear_on_submit=True)
    with form_create:
        title = st.text_input('Enter location', 'location')
        electricity = st.radio(
            "Electricity",
            ('Day', 'Bi', 'Night'))
        gas = st.radio("Gas", ('Yes', 'No'))
        water = st.radio("Water", ('Yes', 'No'))
        cols = ['date']
        if electricity == 'Bi':
            cols.append('day_elec')
            cols.append('night_elec')
        else:
            cols.append('elec')
        if gas == 'Yes':
            cols.append('gas')
        if water == 'Yes':
            cols.append('water')
        submit_create = st.form_submit_button(label="Create")
if submit_create:
    filenames = find_csv_filenames("/home/emeline/PycharmProjects/energy-consumption")
    filepath = 'data_' + title + '.csv'
    if filepath in filenames:
        st.write('This files already exists. Enter a new location.')
    else:
        create_dataset(cols, title)
        st.write('Your file has been successfully created.')
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
    file = load_file()
    option = st.selectbox(
        'Year',
        list_years)
    submit_see = st.form_submit_button(label="Show consumption plots")

if submit_see:
    dataset = Dataset(file)
    dataset.load()
    dataset.evaluate_consumption()
    saved_cols = list(dataset.saved_columns)[1:]
    cols = dataset.consumption_columns[1:]
    dataset.filter_year(str(option))
    figures = (setup_bar_chart(dataset.df, 'consumption_month', [new_col], col + str(option))
                for col, new_col in zip(saved_cols, cols))
    for fig in figures:
        st.plotly_chart(fig, use_container_width=True)
