import pandas as pd

class Dataset():

    def __init__(self, filepath):
        self.filepath = filepath

    def load(self):
        self.df = pd.read_csv(self.filepath)

    def fill(self, df2):
        self.df = self.df.append(df2, ignore_index=True)

    def save(self):
        self.df.to_csv(self.filepath, index=False)


