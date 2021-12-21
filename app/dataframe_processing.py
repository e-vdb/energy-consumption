import pandas as pd
from dateutil.relativedelta import relativedelta

class Dataset():

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        self.df = pd.read_csv(self.filepath, parse_dates=['date'], date_parser=pd.to_datetime)
        self.saved_columns = self.df.columns

    def fill(self, df2):
        self.df = self.df.append(df2, ignore_index=True)
        self.df['date'] = pd.to_datetime(self.df['date'])

    def save(self):
        self.df.to_csv(self.filepath, index=False)

    def sort_by_date(self):
        self.df.sort_values(by='date', inplace=True)

    def add(self, df2):
        self.fill(df2)
        self.sort_by_date()
        self.save()

    def consumption(self, new_col, col_index):
        self.df[new_col] = self.df[col_index].diff()
        self.df['consumption_month'] = self.df['date'].apply(lambda x: x - relativedelta(months=1)).dt.month_name()

    def evaluate_consumption(self):
        self.consumption_columns = []
        for col in self.df.columns:
            new_col = col + '_consumption'
            self.consumption_columns.append(new_col)
            self.df[new_col] = self.df[col].diff()
        self.df['consumption_month'] = self.df['date'].apply(lambda x: x - relativedelta(months=1)).dt.month_name()
        self.df['consumption_year'] = self.df['date'].apply(lambda x: x - relativedelta(months=1)).dt.year

    def set_index_date(self):
        self.df.set_index('date', inplace=True)

    def filter_year(self, year):
        filt = (self.df['date'] >= year + '-02-01') & (self.df['date'] < str(int(year) + 1) + '-02-01')
        df_filter = self.df.loc[filt]
        return df_filter

