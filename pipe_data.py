import pandas as pd

file1 = 'pipes_year.csv'
file2 = 'noky_pipes_inp.txt'

year = pd.read_csv(file1, header=0, usecols=[0,2], names=['YEARCON', 'DC_ID'])
pipes = pd.read_csv(file2, sep="\t", header=0, names=['ID', 'Node1', 'Node2', 'Length', 'Diameter', 'Roughness', 'Material', 'MinorLoss', 'Status'])

df_y = pd.DataFrame(year)
df_p = pd.DataFrame(pipes)
df_y.set_index('DC_ID', inplace=True)
df_p.set_index('ID', inplace=True)
print(df_y.index, df_p.index)
df_j = df_p.join(df_y, how='outer', on='ID')
df_j.to_csv('noky_pipe_year_rough.csv', sep=' ')
