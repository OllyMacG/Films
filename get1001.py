import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import json
import sys, getopt, pprint
from pymongo import MongoClient

URL = 'https://en.wikipedia.org/wiki/1001_Movies_You_Must_See_Before_You_Die'
response = requests.get(URL)
soup = BeautifulSoup(response.text,'html.parser')

table = soup.find('table',{'class':'wikitable sortable collapsible collapsed'}).tbody

rows = table.find_all('tr')

columns = ['Year', 'Title', 'Director', 'Country']
df = pd.DataFrame(columns=columns)

def removeNewLine(value):
    return value.replace('\n',"")

for i in range(1,len(rows)):
    tds = rows[i].find_all('td')

    if len(tds)==4:
        values = [removeNewLine(tds[0].text), removeNewLine(tds[1].text), removeNewLine(tds[2].text), removeNewLine(tds[3].text)]
        df = df.append(pd.Series(values, index=columns), ignore_index=True)
    else:
        print("Not 4 rows")


mongo_client=MongoClient() 
client = MongoClient("mongodb://127.0.0.1:27017")
db=client.Films
collection = db.thousand_and_one_films
collection.drop()
collection.update_many({},{"$set" : {"Oll":1}})
collection.insert_many(df.to_dict('records'))  
print("Connection Successful")
client.close()
# db=mongo_client.thousand_and_one_films
# db.segment.drop()
# header= [ "Year", "Title", "Director", "Country"]

# db.insert_many(df.to_dict('records'))  

# df.to_csv(r'C:\Users\Desktop\'+'\\report.csv',index=False)