import pandas as pd
df = pd.read_excel('ABC.xlsx', nrows=0)
print('Columnas disponibles:', df.columns.tolist())