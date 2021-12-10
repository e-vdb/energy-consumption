import pandas as pd

cols = ['date', 'day_elec', 'night_elec', 'gas', 'water']
data = ([] for col in cols)
dic = {col: val for col, val in zip(cols, data)}
df = pd.DataFrame(dic)
df.to_csv('data.csv', index=False)

