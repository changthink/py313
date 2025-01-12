# -*- coding: utf-8 -*-


from sqlalchemy import create_engine
import pymysql
import pandas as pd


#1. pymysql
conn = pymysql.connect(host='180.65.243.212', port=3307, user='changthink', password='Sunchang11**', db='rp', charset='utf8')
cur = conn.cursor()
sql_del = "delete from bunyang where 기준월 >= '2025-01-31';"
sql_sel = "select * from bunyang where 기준월 >= '2024-12-31';"
sql_ins = "insert into cpi (기준월, 소비자물가지수) values ('2024-11-30', '150.00');"

cur.execute(sql_ins)
conn.commit()     #insert, update, delete와 같은 데이터조작(dml) 문장의 경우, commit를 해줘야 함

df = pd.read_sql_query(sql, conn)
conn.close()


#2. sqlalcehmy(create engine)
engine = create_engine("mysql+pymysql://changthink:Sunchang11**@180.65.243.212:3307/rp")
sql_sel = "select * from cpi where 기준월 > '2024-01-31';"
df1 = pd.read_sql(sql_sel, con = engine)
engine.dispose()  #연결종료

import seaborn as sns
df2 = sns.load_dataset('iris')
engine = create_engine("mysql+pymysql://changthink:Sunchang11**@180.65.243.212:3307/rp")
df2.to_sql('iris', con=engine, index=False, if_exists = 'replace')
engine.dispose()



