import csv
import sqlite3

# 데이터베이스에 연결
con = sqlite3.connect('data.db')
cursor = con.cursor()

# 테이블 생성
cursor.execute('''
                CREATE TABLE menu(
                id int,
                category text, 
                category_num int,
                degree text,
                name text,
                price int,
                info text
                )''')

#csv 파일 읽기 및 데이터베이스에 삽입
with open('data.csv', 'r') as file:
    csv_data = csv.reader(file)
    next(csv_data) # 첫번째 행은 헤더이므로 건너뜀
    for row in csv_data:
        cursor.execute('INSERT INTO menu VALUES (?, ?, ?, ?, ?, ?, ?)', row)

#변경사항 저장 및 연결 종료
con.commit()
con.close()