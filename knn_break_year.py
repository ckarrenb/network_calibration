from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np

train_file = pd.read_csv('pipe_data.csv', header=0, skip_blank_lines=True)
noky_file = pd.read_csv('noky_pipes_02.csv', header=0)

train_data = pd.DataFrame(train_file)
train_data.dropna(axis=0, inplace=True)

noky_data = pd.DataFrame(noky_file)
noky_data.dropna(axis=0, inplace=True)

X = train_data[['install_year', 'diameter']]
y = train_data['break_age']

noky_data_Y = noky_data[['YEARCON', 'SIZE']]
noky_data_Y['YEARCON'] = noky_data['YEARCON'].astype(int)
noky_data_Y.columns = ['install_year', 'diameter']

neighbors = KNeighborsRegressor(n_neighbors=5)
neighbors.fit(X, y)
pred_break = neighbors.predict(noky_data_Y)
noky_data['break_age'] = pred_break
noky_data['break_year'] = noky_data['YEARCON'] + noky_data['break_age'] 
# noky_data.to_csv('noky_synth_breaks_02.csv')
# print(noky_data.head())
