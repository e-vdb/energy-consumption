import pandas as pd

electric_meter = {
    'date': [],
    'day_record': [],
    'night_record': []
}

gas_meter = {
    'date':  [],
    'record': []
}

water_meter = {
    'date': [],
    'record': []
}

df = pd.DataFrame(water_meter)

df.to_csv('data_water.csv', index=False)

