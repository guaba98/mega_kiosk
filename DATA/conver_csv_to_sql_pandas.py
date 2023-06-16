import pandas as pd
import sqlite3

# pandas 라이브러리를 사용해 csv -> sqlite 데이터베이스 변형
con = sqlite3.connect('data.db')

# read_csv() 함수를 사용해 csv파일 읽기
df = pd.read_csv('order_table.csv', encoding='utf-8') # 오류가 나면 utf-8 인코딩을 변경하면 됨

# to_sql() 함수를 사용하여 데이터를 sqlite에 삽입
# to_sql(테이블이름, db, 만약 존재한다면= 교체, index컬럼 생성x)
df.to_sql('order_table', con=con, if_exists='replace', index=False)

#데이터베이스 연결 종료
con.close()
