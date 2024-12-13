import requests
import datetime
import sqlite3
import time
import pandas as pd
from sql_con import get_con
import procedure
import logging
import veriable
import auth

def log(flnm: str):
    fullname = veriable.log_loc+"\\"+"Logs\\"+flnm+".log"
    logging.basicConfig(level=logging.INFO, filename=fullname, filemode='a', format='%(asctime)s -- %(levelname)s -- %(message)s')
    return logging

current_file = 'OMS'
logging = log(current_file)

from datetime import date as dt
from dateutil.relativedelta import relativedelta

td = dt.today()
tdymd = td.strftime("%Y-%m-%d")
dt45 = td - relativedelta(days=46)
dt45 = dt45.strftime("%Y-%m-%d")

usr = auth.omuni_usr
passwd = auth.omuni_passwd

def get_token(table):
    connection = sqlite3.connect('token_omuni.db',
                             detect_types=sqlite3.PARSE_DECLTYPES |
                             sqlite3.PARSE_COLNAMES)
    cursor = connection.cursor()
    insertQuery = f"""INSERT INTO {table}
    VALUES (?, ?, ?);"""

    url = 'https://api.omuni.com/bb/users/business-user/token'
    currentDateTime = datetime.datetime.now()
    headers = {
    'Content-Type': 'application/json'}
    payload = {"grant_type":"password","username":usr,"password":passwd}
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        # print(data)
        cursor.execute(insertQuery, (currentDateTime, data['data']['access_token'], data['data']['refresh_token']))
        connection.commit()
        token =  data['data']['access_token']
    else:
        print(response.status_code)
        print(response.content)
        exit()

    cursor.close()
    connection.close()

    return token

def gen_report(token, start_date, end_date, email):
    url = f"https://api.omuni.com/d/api/oms/oms/consignment/new/download?orderDateStart={start_date}T18:30:00.860Z&orderDateEnd={end_date}T18:29:59.860Z&sendTo="
    url += email
    headers = {'Accept': 'application/json, text/plain, */*', 'Authorization': f"Bearer {token}"}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.content
        print(data)
    else:
        print(response.status_code)
        print(response.content)
        exit()
    return data

def download_report(data):
    url = f'https://s3-ap-south-1.amazonaws.com/ail-mbo-oms-file-download/downloads/{data}.csv'
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        with open(f"{veriable.location}/{data}.csv", "wb") as file:
            file.write(response.content)
            print("File downloaded successfully!")
    else:
        print("Failed to download the file.")
        print(response.status_code)
        print(response.content)
        exit()


logging.info("generating file")
token = get_token('token')
report = gen_report(token , dt45, tdymd, 'email address to send the file')
time.sleep(60)
data = report.decode('utf-8')

downloaded = 0
while downloaded == 0:
    try:
        download_report(data)
        downloaded = 1
    except:
        logging.exception('ERROR')
        time.sleep(30)
        logging.info("Retrying")


def load_data(filepath):
    df = pd.read_csv(f"{veriable.location}/{filepath}.csv", usecols=[n for n in range(0,24)])
    connection  = get_con(veriable.database)
    cursor = connection.cursor()
    cursor.execute(f''' delete from {veriable.table} ''')
    cursor.commit()
    cursor.fast_executemany = True
    query = f''' INSERT INTO {veriable.table}
    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
    '''
    all_df = df.fillna('')
    df_list = all_df.values.tolist()
    all_df = procedure.fill_null(df_list)
    all_df = procedure.fill_NaT(df_list)
    for i in range(0, len(all_df), 25000):
        cursor.executemany(query, all_df[i:i + 25000])
        print(i)
        cursor.commit()
    print(len(df_list))
    cursor.commit()
    cursor.close()
    connection.close()

if __name__ == "__main__":
    load_data(data)









