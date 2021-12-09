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

dataset_names = ['electric', 'gas', 'water']
dataset= [electric_meter, gas_meter, water_meter]
for name, data in zip(dataset_names, dataset):
    df = pd.DataFrame(data)
    filename = 'data_' + name + '.csv'
    df.to_csv(filename, index=False)

