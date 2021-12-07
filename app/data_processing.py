import pandas as pd

electric_meter = {
    'date': [],
    'day_record': [],
    'night_record': []
}

df = pd.DataFrame(electric_meter)

df.to_csv('data.csv', index=False)

