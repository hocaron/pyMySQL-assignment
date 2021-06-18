#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pymysql

db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', charset='utf8')

cursor = db.cursor()

sql = 'CREATE DATABASE coronaVaccine'

cursor.execute(sql)

db.commit()


# In[2]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
cursor = db.cursor()

sql = '''
CREATE TABLE corona (
서울시기준일 VARCHAR(30) NOT NULL PRIMARY KEY,
서울시확진자  INT(20) NOT NULL,
서울시추가확진 INT(20) NOT NULL
)
'''

cursor.execute(sql)

db.commit()
db.close()


# In[3]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
cursor = db.cursor()

sql = '''
CREATE TABLE vaccine (
접종일 VARCHAR(30) NOT NULL,
접종대상자  INT(20) NOT NULL,
당일일차접종자수 INT(20) NOT NULL,
일차접종누계 INT(20) NOT NULL,
일차접종률 FLOAT(5, 1),
당일이차접종자수 INT(20) NOT NULL,
이차접종누계 INT(20) NOT NULL,
이차접종률 FLOAT(5, 1),
FOREIGN KEY(접종일)
    REFERENCES corona(서울시기준일)
)
'''

cursor.execute(sql)

db.commit()
db.close()


# In[4]:


import pandas as pd

db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
cursor = db.cursor()

data = pd.read_csv('서울특별시 코로나19 확진자 발생동향.csv', encoding='cp949')

sql = "INSERT INTO corona (서울시기준일, 서울시확진자, 서울시추가확진) VALUES (%s, %s, %s)"

for i in range(len(data)):
    cursor.execute(sql, (str(data['서울시기준일'][i]), int(data['서울시확진자'][i]), int(data['서울시추가확진'][i])))

db.commit()
db.close()


# In[5]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
cursor = db.cursor()

data = pd.read_csv('서울특별시 코로나19 백신 예방접종 현황.csv', encoding='cp949')

sql = "INSERT INTO vaccine (접종일, 접종대상자, 당일일차접종자수, 일차접종누계, 일차접종률, 당일이차접종자수, 이차접종누계,이차접종률) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

for i in range(len(data)):
    cursor.execute(sql, (str(data['접종일'][i]), int(data['접종대상자'][i]), int(data['당일일차접종자수'][i]), int(data['일차접종누계'][i]), float(data['일차접종률'][i]), int(data['당일이차접종자수'][i]),
                        int(data['이차접종누계'][i]), float(data['이차접종률'][i])))
db.commit()
db.close()


# In[6]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
SQL = '''SELECT * FROM corona;'''
corona = pd.read_sql(SQL, db)


# In[7]:


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

x = pd.date_range(corona.서울시기준일[0], corona.서울시기준일[len(corona) - 1])
y = corona.서울시확진자
plt.plot(x, y)
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.title('Corona cases on the rise')


# In[8]:


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

x = pd.date_range(corona.서울시기준일[0], corona.서울시기준일[len(corona) - 1])
y = corona.서울시추가확진
plt.plot(x, y)
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(30))
plt.title('Corona additional cases')


# In[9]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
SQL = '''SELECT 접종일 FROM vaccine;'''
vaccine_date = pd.read_sql(SQL, db)
SQL = '''SELECT 일차접종누계 FROM vaccine ORDER BY 일차접종누계 ASC;'''
vaccine_1 = pd.read_sql(SQL, db)
SQL = '''SELECT 이차접종누계 FROM vaccine ORDER BY 이차접종누계 ASC;'''
vaccine_2 = pd.read_sql(SQL, db)


# In[10]:


import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as ticker
import numpy as np

x = pd.date_range(vaccine_date.접종일[0], vaccine_date.접종일[len(vaccine_date) - 1])
y = vaccine_1
z = vaccine_2
plt.figure(1)
plt.plot(x, y)
plt.plot(x, z)
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.title('Corona vaccine')
plt.legend(["Vaccine primary dose rate", "Vaccine secondary dose rate"])

x = pd.date_range(vaccine_date.접종일[0], vaccine_date.접종일[len(vaccine_date) - 1])
k = corona.서울시추가확진.loc[442:481]
plt.figure(2)
plt.plot(x, k)
plt.xticks(rotation=45)
ax=plt.gca()
ax.xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.title('Corona additional cases')


# In[11]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
SQL = '''SELECT 서울시기준일 FROM corona WHERE 서울시추가확진 > 500;'''
print("서울시 코로나 추가 확진자 500명이 넘은 날짜")
corona_max500 = pd.read_sql(SQL, db)
corona_max500


# In[12]:


db = pymysql.connect(host='localhost', port=3306, user='root', password='1234', db='coronaVaccine' ,charset='utf8')
SQL = '''SELECT 서울시기준일, 서울시추가확진, 일차접종률, 이차접종률 FROM corona, vaccine WHERE corona.서울시기준일 = vaccine.접종일;'''
print("서울시 코로나 추가 확진자와 백신 접종률")
corona_max500 = pd.read_sql(SQL, db)
corona_max500


# In[ ]:




