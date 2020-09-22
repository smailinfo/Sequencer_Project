import datetime
import subprocess
import time
import psycopg2
from prettytable import PrettyTable
from termcolor import colored
from datetime import datetime, timedelta ,timezone
import os



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



#print(date_now)

col_names = []

#date1=date(4:25:41.500101)


dt = datetime(2010, 2, 25, 23, 23)
dr=time.mktime(dt.timetuple())



#print('type dt', type(dt))
#print(dr)
while True:
    sql = (f'''SELECT task_number , task_name , task_time  FROM groundstation.sequencer_auto 
    where sequencer_auto."task_time" > now() at time zone 'utc'
    ''')
    curr.execute(sql)
    rows = curr.fetchall()

    x = PrettyTable(['task_number','task_name','task_date','remaining_time'])

    for elt in rows:
        date_now = datetime.now()
        elt_unix_time = time.mktime(elt[2].timetuple())
        date_now = time.mktime(date_now.timetuple())
        remaining_time = elt_unix_time - date_now
        tab=[elt[0],elt[1],elt[2],remaining_time]

        if remaining_time==0:
            os.system(f"python /home/cgs/PycharmProjects/Sequencer/test_task.py {elt[0]} {elt[1]} ")
            print('OK')
        else:
            pass



        x.add_row(tab)
        #x.add_row(time_delta)

    print(x.get_string())

    time.sleep(0.5)


'''
while True:
    print("slm")


    time.sleep(3)

'''
#t1 = threading.Thread(target=insert_line_dict, args=(sequence_task,))
#t1.start()      # starting thread 1

