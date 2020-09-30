import datetime
import subprocess
import threading
import time
import psycopg2
from prettytable import PrettyTable
from termcolor import colored
from datetime import datetime, timedelta ,timezone
import os
import queue
from queue import Queue

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






while True:
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
        where planifier."task_time_start" > now() at time zone 'utc'
        order by planifier."task_time_start"
        limit 20
        ''')
    curr.execute(sql)
    rows = curr.fetchall()
    date_now = datetime.now()
    date_now = time.mktime(date_now.timetuple())
    x = PrettyTable(['task_number','task_name','task_date','remaining_time'])

    i=0
    for row in rows :
        row_unix_time = time.mktime(row[2].timetuple())
        remaining_time = row_unix_time - date_now
        tab=[row[0],row[1],row[2],remaining_time]


        if remaining_time>0:
            x.add_row(tab)
            print(x.get_string())
            #break


        elif remaining_time==0:
            os.system(f"python /home/cgs/PycharmProjects/Sequencer/test_task.py {row[0]} {row[1]} ")
            x.add_row(tab)
            print(x.get_string())
            print('OK')
            break








    time.sleep(0.5)








'''
        if remaining_time==0:
            os.system(f"python /home/cgs/PycharmProjects/Sequencer/test_task.py {row[0]} {row[1]} ")
            print('OK')
            pro()
        else:
            pass


        x.add_row(tab)
        print(x.get_string())

    time.sleep(0.5)
    


'''

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

