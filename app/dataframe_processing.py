import pandas as pd
import datetime

class Dataset():

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        self.df = pd.read_csv(self.filepath, date_parser=pd.to_datetime)

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

    def set_index_date(self):
        self.df.set_index('date', inplace=True)

    def filter_year(self, year):
        filt = (self.df['date'] >= year + '-01-01') & (self.df['date'] <= year + '-12-31')
        self.df = self.df.loc[filt]