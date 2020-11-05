# -*- coding: utf-8 -*-
"""

@author: Алина
"""
import requests
import json
import time
import re
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup as bs
from collections import Counter 

def getPage(page = 0):
    params = {'text': 'NAME:IT', 'area': [1,2,3], 'page': page, 'per_page': 100 }    
    req = requests.get('https://api.hh.ru/vacancies', params)
    data = req.content.decode()
    req.close()
    return data

def ReadWriteVac(clmn, vacance):
    req = requests.get(f'https://api.hh.ru/vacancies/{vacance["id"]}') 
    data = req.content.decode()
    jsObj1 = json.loads(data)
    o = t = u = -10
    flag = True
    try:
        Vname = jsObj1['name']
        city = None
        minSalary = None
        maxSalary = None
        Cname = None
        skills = ''
        exp = None
        employ = None
        jobgraph = None
        desc = None
        duties = None
        terms = None
        requirements = None
        date = jsObj1['published_at']
        
        for i in jsObj1['key_skills']:
            skills+=f' {i["name"]};'
        if jsObj1['area'] is not None:
            city = jsObj1['area']['name']
        if jsObj1['salary'] is not None:
            minSalary = jsObj1['salary']['from']
            maxSalary = jsObj1['salary']['to']
        if jsObj1['employer'] is not None:
            Cname = jsObj1['employer']['name']
        if jsObj1['experience'] is not None:
            exp = jsObj1['experience']['name']
        if jsObj1['employment'] is not None:
            employ = jsObj1['employment']['name']
        if jsObj1['schedule'] is not None:
            jobgraph = jsObj1['schedule']['name']
       
        descrip = jsObj1['description']
        soup = bs(descrip, "html.parser")
        for p in soup:
            if (flag and str(p).lower().find('обязанности')==-1 and 
                        str(p).lower().find('условия')==-1 and 
                        str(p).lower().find('требования')==-1):
                        desc = re.sub('<[^<]+?>', ' ', str(p))
                        flag = False
            if (o==-1):
                duties = re.sub('<[^<]+?>', ' ', str(p))
            if (t==-1):
                requirements = re.sub('<[^<]+?>', ' ', str(p))
            if (u==-1):
                terms = re.sub('<[^<]+?>', ' ', str(p))
           
            if str(p).lower().find('обязанности')!=-1:
                o=1
            if str(p).lower().find('требования')!=-1:
                t=1
            if str(p).lower().find('условия')!=-1:
                u=1
            o-=1
            t-=1
            u-=1
    except:
        print('Пропущена запись')
    req.close()
    return [pd.Series([Vname, city, minSalary, maxSalary,Cname,
            date, exp, employ, jobgraph, desc,
            duties, requirements, terms, skills], index = clmn)]
df = pd.DataFrame({
     'Name':[],
     'City':[],
     'MinSalary':[],
     'MaxSalary':[],
     'Company':[],
     'Date':[],
     'Expirience':[],
     'Employment':[],
     'WorkSchedule':[],
     'Descriptions':[],
     'Duties':[],
     'Requiremenst':[],
     'Terms':[],
     'KeySkills':[]
      })
   
clmn = df.columns
for page in range(0, 20):
    jsObj = json.loads(getPage(page))
    for item in jsObj['items']:
       df = df.append(ReadWriteVac(clmn,item), ignore_index=True)
    if (jsObj['pages'] - page) <= 1:
        break
    time.sleep(0.5)
    print((page+1)*100,' получено')
df.to_csv('parse.csv')  
print('Старницы поиска собраны')