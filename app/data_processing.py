import pandas as pd

def create_dataset(cols, filename):
    data = ([] for col in cols)
    dic = {col: val for col, val in zip(cols, data)}
    df = pd.DataFrame(dic)
    filepath = 'data_' + filename + '.csv'
    df.to_csv(filepath, index=False)
