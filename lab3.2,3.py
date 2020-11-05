# -*- coding: utf-8 -*-
"""

@author: Алина
"""

import pandas as pd
import datetime as dt
from collections import Counter 

df = pd.read_csv('parse.csv')
df['MinSalary'] = df['MinSalary'].fillna(0)
df['MaxSalary'] = df['MaxSalary'].fillna(df['MinSalary'])
df = df.sort_values(by='MaxSalary')
df = df.sort_values(by='MinSalary')
grMaxSal=[0, 30000, 600000, 120000, 150000, 180000, 210000, 240000, 270000, 300000]
df_arr = []

for value in grMaxSal:
    if value == 300000:
        df_arr.append(df[(df['MaxSalary'] >= value)])
        break
    df_arr.append(df[(df['MaxSalary'] >= value) & (df['MaxSalary'] < (value + 30000))])

index=-1
for df_ in df_arr:
    index+=1
    if index!=9:
        print(f'группа {grMaxSal[index]}-{grMaxSal[index]+30000}')
    else:
        print(f'группа {grMaxSal[index]}- ... ')
    print('Пункт a')
    uniq = df_['Name'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Name'].str.lower() == value])
        print(f' У {value} - {cnt} повт.')
    print('Пункт b')
    date_arr = []
    for date in df_['Date']:
        delta = dt.date.today() - dt.datetime.strptime(date.split('T')[0], "%Y-%m-%d").date()
        date_arr.append(int(str(delta).split()[0]))
        print(f'max = {max(date_arr)} min ='
          f' {min(date_arr)} avg = {sum(date_arr)/len(date_arr)}')
    print('Пункт c')
    uniq = df_['Expirience'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Expirience'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Пункт d')
    uniq = df_['Employment'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Employment'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Пункт e')
    uniq = df_['WorkSchedule'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['WorkSchedule'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    print('Пункт f')
    kSkill = []
    for value in df_['KeySkills']:
        val_arr = str(value).split(';')
        for v in val_arr:
            kSkill.append(v.lower())
    kSkill = [value for value in kSkill if value]
    print(Counter(kSkill))
print('Часть 3')

df_arr = []
uniq = df['Name'].str.lower().unique()

for value in uniq:
    df_arr.append(df[(df['Name'].str.lower() == value)])
for df_ in df_arr:
    print(f'вакансия {df_["Name"].values[0]}')
    print('Задание 1')
    max_uniq = df_['MaxSalary'].unique()
    min_uniq = df_['MinSalary'].unique()
    for value in max_uniq:
        cnt = len(df_.loc[df['MaxSalary'] == value])
        print(f' У max {value} - {cnt} повт.')
    for value in min_uniq:
        cnt = len(df_.loc[df['MinSalary'] == value])
        print(f' У min {value} - {cnt} повт.')

    print('Задание 2')
    date_arr = []
    for date in df_['Date']:
        delta = dt.date.today() - dt.datetime.strptime(date.split('T')[0], "%Y-%m-%d").date()
        date_arr.append(int(str(delta).split()[0]))
        print(f'max = {max(date_arr)} min ='
          f' {min(date_arr)} avg = {sum(date_arr)/len(date_arr)}')

    print('Задание 3')
    uniq = df_['Expirience'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Expirience'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 4')
    uniq = df_['Employment'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['Employment'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 5')
    uniq = df_['WorkSchedule'].str.lower().unique()
    for value in uniq:
        cnt = len(df_.loc[df['WorkSchedule'].str.lower() == value])
        print(f'{value} - {cnt} повт.')
    
    print('Задание 6')
    kSkill = []
    for value in df_['KeySkills']:
        val_arr = str(value).split(';')
        for v in val_arr:
            kSkill.append(v.lower())
    kSkill = [value for value in kSkill if value]
    print(Counter(kSkill))
print('Выполнено')