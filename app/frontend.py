import streamlit as st
from dataframe_processing import Dataset
import pandas as pd
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

def plot_consumption(df, x, cols):
    elec_col = [col for col in cols if 'elec' in col]
    gas_water = [col for col in cols if 'elec' not in col]
    figures_elec = setup_bar_chart(df, x, elec_col, 'Electricity consumption (kWh)')
    figures_gas_water = [setup_bar_chart(df, x, [new_col], dic_name[new_col])
               for new_col in gas_water]
    figures = [figures_elec] + figures_gas_water
    for fig in figures:
        st.plotly_chart(fig, use_container_width=True)

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
expander_fill = st.expander('Open to fill your index')
with expander_fill:
    form = st.form(key="my_form", clear_on_submit=True)
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
    st.success('Your entry has been added.')

st.header('Total consumption')
if dataset.df.empty:
    st.warning('No data stored! Please fill first your index.')
else:
    dataset.evaluate_consumption()
    cols = dataset.consumption_columns[1:]
    saved_cols = list(dataset.saved_columns)[1:]
    tot_cons_per_year = dataset.df.groupby('consumption_year')[cols].sum()

    tot_cons_per_year = tot_cons_per_year.reset_index()
    plot_consumption(tot_cons_per_year, 'consumption_year', cols)

    tot_cons_per_year.rename(columns=dic_name, inplace=True)
    tot_cons_per_year.set_index('consumption_year', inplace=True)
    st.write(tot_cons_per_year)

st.header('Monthly consumption')
form_visual = st.form(key="my_form_visual", clear_on_submit=True)

with form_visual:
    if dataset.df.empty:
        st.warning('No data stored! Please fill first your index.')
    else:
        list_years = [i for i in range(dataset.df['date'].dt.year.min(), dataset.df['date'].dt.year.max() + 1)]
        option = st.selectbox(
            'Year',
            list_years)
    submit_see = st.form_submit_button(label="Show consumption plots")

if submit_see and not dataset.df.empty:
    st.subheader(f"Consumption for year {option}")
    saved_cols = list(dataset.saved_columns)[1:]
    df_filter = dataset.filter_year(str(option))
    plot_consumption(df_filter, 'consumption_month', cols)


st.header('Compare consumption')
form_comp = st.form(key="my_form_comp", clear_on_submit=True)
with form_comp:
    if dataset.df.empty:
        st.warning('No data stored! Please fill first your index.')
    else:
        st.write('Select the year for which you want a comparison with previous years')
        year1 = st.selectbox('Year', list_years[1:])
        df_year = dataset.df.groupby('consumption_year')
        saved_cols = list(dataset.saved_columns)
        df1 = df_year.get_group(year1).drop([*saved_cols, 'date_consumption', 'consumption_year'], axis=1)
        df1.set_index('consumption_month', inplace=True)
        df1.rename(columns=dic_name, inplace=True)
    submit_comp = st.form_submit_button(label="Compare consumption")

if submit_comp and not dataset.df.empty:
    index = list_years.index(year1)
    for year2 in list_years[0:index]:
        df2 = df_year.get_group(year2).drop([*saved_cols, 'date_consumption', 'consumption_year'], axis=1)
        df2.set_index('consumption_month', inplace=True)
        df2.rename(columns=dic_name, inplace=True)
        st.subheader(f'Comparison between {year1} and {year2}')
        diff = (df1 - df2).dropna(axis=0)
        st.dataframe(diff.style.background_gradient(axis=0, cmap='RdYlGn_r'))
