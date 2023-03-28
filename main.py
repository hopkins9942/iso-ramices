import numpy as np
import pandas as pd

# data = np.genfromtxt('../GCEModel/Enrichment_Log_ColdGas.txt', delimiter=',', names=True)
df = pd.read_csv('../GCEModel/Enrichment_Log_ColdGas.txt', skipinitialspace=True)

print(df)
# print(data.colnames)
print(df.iloc[0])

print(df.columns)

print(df['RingIndex'][30:60])
print(df['RingRadius'][30:60])


mask = (df['RingIndex']==40)

print(df[mask])

print(df[mask]['Time'][-10:], df[mask]['Stellar_Fe'][-10:])
# print(data['Time'])
# print(dataTotal)



