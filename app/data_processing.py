import pandas as pd

def create_dataset(cols, filename):
    data = ([] for col in cols)
    dic = {col: val for col, val in zip(cols, data)}
    df = pd.DataFrame(dic)
    filepath = 'data_' + filename + '.csv'
    df.to_csv(filepath, index=False)

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]
