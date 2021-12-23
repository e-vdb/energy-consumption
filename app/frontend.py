import streamlit as st
from dataframe_processing import Dataset
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta
from graphic import setup_bar_chart
from data_processing import find_csv_filenames, create_dataset
st.set_page_config(layout="wide")


def load_file():
    return find_csv_filenames("/home/emeline/PycharmProjects/energy-consumption")

dic_name = {'elec_consumption': 'Electricity consumption (kWh)',
            'day_elec_consumption': 'Electricity day consumption (kWh)',
            'night_elec_consumption': 'Electricity night consumption (kWh)',
            'gas_consumption': 'Gas consumption (m3)',
            'water_consumption': 'Water consumption (m3)'}

filenames = load_file()

class App:
    def __init__(self, filepath):
        self.fetch_data(filepath)

    def fetch_data(self, filepath):
        self.data = Dataset(filepath)
        self.data.load()

# Set the app title
st.title("Energy consumption")
st.write("Save and visualise your energy consumption")

st.sidebar.header('Create a new file')
expander = st.sidebar.expander('Select data to record')
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
    filepath = 'data_' + title + '.csv'
    if filepath in filenames:
        st.sidebar.error('This files already exists. Enter a new location.')
    else:
        create_dataset(cols, title)
        st.sidebar.success('Your file has been successfully created.')
        filenames = load_file()


st.sidebar.header('Select your file')
file = st.sidebar.selectbox('Files', filenames)
dataset = App(file).data

st.header('Fill your index')
form = st.form(key="my_form", clear_on_submit = True)
with form:
    d = st.date_input(
        "Date",
        value=pd.to_datetime("2021-12-01", format="%Y-%m-%d"))
    saved_cols = list(dataset.saved_columns)[1:]
    data_input = [st.number_input(col) for col in saved_cols]
    submit = st.form_submit_button(label="Add")

if submit:
    data = [d] + data_input
    newline = {col: val for col, val in zip(cols, data)}
    dataset.add(newline)

st.header('Total consumption')
if dataset.df.empty:
    st.warning('No data stored!')
else:
    dataset.evaluate_consumption()
    cols = dataset.consumption_columns[1:]
    tot_cons_per_year = dataset.df.groupby('consumption_year')[cols].sum()
    tot_cons_per_year.rename(columns=dic_name, inplace=True)
    st.write(tot_cons_per_year)


st.header('Plot consumption')
form_visual = st.form(key="my_form_visual", clear_on_submit=True)

with form_visual:
    if dataset.df.empty:
        st.warning('No data stored!')
    else:
        list_years = [i for i in range(dataset.df['date'].dt.year.min(), dataset.df['date'].dt.year.max() + 1)]
        option = st.selectbox(
            'Year',
            list_years)
    submit_see = st.form_submit_button(label="Show consumption plots")

if submit_see:
    if dataset.df.empty:
        st.warning('No data stored!')
    else:
        st.subheader(f"Consumption for year {option}")
        saved_cols = list(dataset.saved_columns)[1:]
        df_filter = dataset.filter_year(str(option))
        figures = (setup_bar_chart(df_filter, 'consumption_month', [new_col], col + str(option))
                    for col, new_col in zip(saved_cols, cols))
        for fig in figures:
            st.plotly_chart(fig, use_container_width=True)

