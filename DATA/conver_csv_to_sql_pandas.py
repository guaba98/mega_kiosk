import pandas as pd
import sqlite3

con = sqlite3.connect('data.db')
df = pd.read_csv('data.csv', encoding='cp949')
df.to_sql('menu', con=con, if_exists='replace', index=False)
con.close()
