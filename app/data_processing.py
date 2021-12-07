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

df = pd.DataFrame(gas_meter)

df.to_csv('data_gas.csv', index=False)

