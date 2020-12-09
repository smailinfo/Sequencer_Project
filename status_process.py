import datetime
import subprocess
import threading
import time
import psycopg2
import multiprocessing
from prettytable import PrettyTable
from termcolor import colored
from datetime import datetime, timedelta ,timezone
import os
import queue
from queue import Queue
import sched
from configparser import SafeConfigParser , ConfigParser
class connexion:
    def __init__(self):
        self.con = psycopg2.connect(database="alsat_2a", user="postgres", password="cgs", host="localhost", port="5432")
        self.cur = self.con.cursor()

    print(colored("Database opened with successufully","green"))

    def close(self):
        self.close = self.con.close()

    def commit(self):
        self.com = self.con.commit()

coonn = connexion()
curr = coonn.cur




import time, threading
def foo():
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
               where planifier."task_time_start" > now() at time zone 'utc'
               order by planifier."task_time_start"
               asc limit 5
               ''')
    curr.execute(sql)
    rows = curr.fetchall()
    for row in rows:
        date_now = datetime.now()
        date_now = time.mktime(date_now.timetuple())
        row_unix_time = time.mktime(row[2].timetuple())
        remaining_time = row_unix_time - date_now
        tab = (row[0], row[1], row[2], remaining_time)
        print(tab)
    print(time.ctime())
    threading.Timer(2, foo).start()




def update_column(task_number,status:str=''):
    schema = 'groundstation'
    table_name = 'planifier'
    column='status'
    sql = (f'''update {schema}."{table_name}"  set {column} ='{status}' 
            where {table_name}.task_number = {task_number}''')
    curr.execute(sql)
    coonn.commit()
    print(colored(f"""case is finished""", 'green', attrs=['reverse', 'blink']))





def create_task():
    task_list=[]
    q = queue.Queue()
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
           where planifier."task_time_start" > now() at time zone 'utc'
           order by planifier."task_time_start"
           limit 1
           
           ''')
    curr.execute(sql)
    rows = curr.fetchall()
    for row in rows:
        task_list.append(row)
        q.put(row)




    while not q.empty():
        print ("#####################################################################")
        for head in list(q.queue):
            date_now = datetime.now()
            date_now = time.mktime(date_now.timetuple())
            row_unix_time = time.mktime(head[2].timetuple())
            remaining_time = row_unix_time - date_now
            q_elt = (head[0], head[1], head[2], remaining_time)

            if remaining_time == 0:
                try:
                    configure = ConfigParser()
                    configure.read('tasks.ini')
                    path_script = configure.get(head[1], 'path')
                    print(path_script , head[0] , head [1])
                    os.system(f"python {path_script} {head[0]} {head[1]} ") # TODO create Thread
                    update_column(head[0],'in progress')
                                                                             # TODO insert into sequnecer table
                                                                             # TODO follow thread
                                                                             # TODO put head
                                                                             # TODO insert to runing task table or if head[1] = SSPS -> insert in ssps table
                                                                             # TODO insert to runing task table or if head[1] = SSPS -> insert in media manager (traitement HTMR)table

                    q.get(head)

                except Exception as e:
                    print(colored(f"{e}","red") )
                    q.get(head)
                    q.get(head)

            print(q_elt)
        time.sleep(1)

    create_task()



def create():

    for i in range(1000):
        print(i)


t1 = threading.Thread(target=create_task(), args=())
#t2 = threading.Thread(target=create(), args=())
t1.start()  # starting thread 1
#t2.start()  # starting thread 1

print(threading.get_ident())
#t2 = multiprocessing.Process(target=create2(), args=())
#t1 = multiprocessing.Process(target=create_task(), args=())





#print("**************************************************************")
#create()















###############################################################################################

"""
sql = (f'''SELECT task_number , task_name , task_time  FROM groundstation.sequencer_auto 
    where sequencer_auto."task_time" > now() at time zone 'utc'
    order by sequencer_auto."task_time"
    ''')
curr.execute(sql)
rows = curr.fetchall()

list_queue=[]
q = queue.Queue() #

#x = PrettyTable(['task_number','task_name','task_date'])
for elt in rows:
    q.put(elt)
    #list_queue.append(elt)
for i in q.queue:
    print(i[0],i[1],i[2])

    #x.add_row(elt)
    
"""

###############################################################################################

#run_process()

#t1 = threading.Thread(target=run_process, )
#t1.start()      # starting thread 1

