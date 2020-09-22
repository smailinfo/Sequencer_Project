import os , glob , os.path
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
#configure.read('sequencer.ini')


#
class connexion:
    def __init__(self):
        #database=configure.get('DATABASE', 'database')
        self.con = psycopg2.connect(database="alsat_2a", user="postgres", password="cgs", host="localhost", port="5432")
        self.cur = self.con.cursor()

    print(colored("Database opened with successufully","green"))

    def close(self):
        self.close = self.con.close()

    def commit(self):
        self.com = self.con.commit()


def delete_from_table(schema: str = '', table_name: str = ''):
    coonn = connexion()
    curr = coonn.cur
    curr.execute(f'delete from {schema}."{table_name}" ')
    coonn.commit()

#insert passes  in sequencer_auto table:
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
    print (colored(f'{nbr} task are saved ',"green"))


def remove_files():
    y=0
    file_list=glob.glob(os.path.join('Files','*.txt'))
    for f in file_list:
        #print(f)
        os.remove(f)
        y+=1
    print(colored(f'{y} file are deleted',"red"))


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
    #time_task=datetime.strftime(date_time_task, "%H:%M")
    #subprocess.call(["/home/cgs/Documents/Scripts/Atq_Tool.sh", time_task, date_task, path_task])
    #time.sleep(0.1)
    #task_num = os.popen('atq | cut -f1| sort | tail -1')
    #task_num = random.gauss(0, 2000)
    #task_num = int(task_num.read())
    # create file loge ------------------



    with open (f'Files/act_{task_name}_{number_task}.txt','w') as f:
        f.write(f"""##################################################################################
#  Suivi de passage bande S 
#  Sequencer Version        = 0.1
#  System configuration     = /home/cgs/PycharmProjects/Sequencer/tasks.ini
#  Generation Time    = {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
##################################################################################
""")

        f.write(f"\ntask_name= {task_name}\ntask_time= {time_task}\ntask_number= {number_task}\nsat_name= {line_value_dict['sat_name']}\nsat_id= {line_value_dict['sat_id']}\nstatus= {line_value_dict['status']}\nfile_name= act_{task_name}_{number_task}.txt")


    #print(number_task)
    tup = (number_task,task_name,time_task,line_value_dict['sat_name'], line_value_dict['sat_id'], line_value_dict['station_id'],line_value_dict['status'])
    #tup = (task_name, line_value_dict['sat_name'] ,time_task, line_value_dict['sat_id'],line_value_dict['station_id'],line_value_dict['status'])
    return tup



remove_files()

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


for u in rows:
    #print(u)
    pass

sequence_task=[]
number_task=1

tasks_name=configure.sections()
for line_pass in rows:                          # for each pass we take n task in sequencer.ini file
    for tsk in tasks_name:
        sequence_task.append(task(line_pass,tsk,number_task))
        number_task += 1
        #sequence_task.append(task(line_pass, 'open_RM',number_task))
        #number_task += 1
        #sequence_task.append(task(line_pass, 'open_TM',number_task))
        #number_task += 1
print(colored(f'{number_task-1} task are programmed',"green"))


t1 = threading.Thread(target=insert_line_dict, args=(sequence_task,))
t1.start()      # starting thread 1





