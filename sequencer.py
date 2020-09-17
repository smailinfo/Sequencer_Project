import os
import random
from configparser import ConfigParser

from datetime import datetime, timedelta
import time


import psycopg2
import sys
from termcolor import colored
from prettytable import PrettyTable
import re
import subprocess
import threading



configure = ConfigParser()
configure.read('tasks.ini')

class connexion:
    def __init__(self):
        self.con = psycopg2.connect(database="alsat_2a", user="postgres", password="cgs", host="localhost", port="5432")
        self.cur = self.con.cursor()

    print("Database opened with successufully")

    def close(self):
        self.close = self.con.close()

    def commit(self):
        self.com = self.con.commit()


def delete_from_table(schema: str = '', table_name: str = ''):
    coonn = connexion()
    curr = coonn.cur
    curr.execute(f'delete from {schema}."{table_name}" ')
    coonn.commit()


def insert_line_dict(values):

    schema = 'groundstation'
    table_name = 'sequencer_auto'
    delete_from_table(schema, table_name)
    col_value_dict = {
        'task_number': '',
        'task_name': '',
        'task_time': '',
        'sat_name': '',
        'sat_id': '',
        'station_id': '',
        'status': ''
    }

    coonn = connexion()
    curr = coonn.cur
    columns = list(col_value_dict.keys())
    # values = list(col_value_dict.values())  # liste append

    nbr=0
    for p in values:
        #print(p)
        sql = (f'INSERT INTO {schema}."{table_name}" ("' + '", "'.join(['%s'] * len(columns)) + '"' + ") ") % tuple(
            columns) + "VALUES (" + ", ".join(["%s"] * len(columns)) + ")"
        #print(sql)
        curr.execute(sql, list(p))

        coonn.commit()
        nbr+=1
    print (f'{nbr} of line are saved')



def task(line_pass: tuple,task_name:str='',number_task:int=2):
    line_value_dict = {
        #'task_number': '',
        'task_name': line_pass[0],
        'task_time': line_pass[3],
        'sat_name': line_pass[2],
        'sat_id': line_pass[1],
        'station_id': line_pass[0],
        'status': 'waiting'
    }

    delta_time=int(configure.get(task_name, 'delta_time'))
    AB = configure.get(task_name, 'AB')
    path = configure.get(task_name, 'path')
    duration=configure.get(task_name, 'duration')


    if AB == 'befor':
        time_task=line_value_dict['task_time']- timedelta(minutes=delta_time)
    elif AB=='after':
        time_task = line_value_dict['task_time'] - timedelta(minutes=delta_time)
    else :
        print(colored(f"name {AB} is incorrect" ),"red")

    #duration= datetime.strptime(duration, "%M:%S")

    #date_task=datetime.strftime(date_time_task, "%m/%d/%Y")     # convert time to  str
    #time_task=datetime.strftime(date_time_task, "%H:%M")
    #subprocess.call(["/home/cgs/Documents/Scripts/Atq_Tool.sh", time_task, date_task, path_task])
    #time.sleep(0.1)
    #task_num = os.popen('atq | cut -f1| sort | tail -1')
    #task_num = random.gauss(0, 2000)
    #task_num = int(task_num.read())
    # create file loge ------------------



    with open (f'Files/act_{task_name}_{number_task}.txt','w') as f:
        f.write(f"task_number= {number_task}\nstatus= {line_value_dict['status']}\nfile_name= act_{task_name}_{number_task}.txt")


    print(number_task)
    tup = (number_task,task_name,time_task,line_value_dict['sat_name'], line_value_dict['sat_id'], line_value_dict['station_id'],line_value_dict['status'])
    #tup = (task_name, line_value_dict['sat_name'] ,time_task, line_value_dict['sat_id'],line_value_dict['station_id'],line_value_dict['status'])
    return tup



coonn = connexion()
curr = coonn.cur
sql=(f'''SELECT distinct * FROM groundstation.planing_pass
where planing_pass."AOS" > now() at time zone 'utc'
order by  planing_pass."AOS" 
''')


curr.execute(sql)
rows = curr.fetchall()



col_names = []
for elt in curr.description:
    col_names.append(elt[0])

print(col_names)



# Create the dataframe, passing in the list of col_names extracted from the description


for u in rows:
    print(u)

sequence_task=[]
number_task=1
for line_pass in rows:

    sequence_task.append(task(line_pass,'open_MMCS',number_task))
    number_task += 1
    #sequence_task.append(task(line_pass, 'open_RM',number_task))
    #number_task += 1
    #sequence_task.append(task(line_pass, 'open_TM',number_task))
    #number_task += 1
print(number_task-1)


t1 = threading.Thread(target=insert_line_dict, args=(sequence_task,))
t1.start()      # starting thread 1
#insert_line_dict(sequence_task)






