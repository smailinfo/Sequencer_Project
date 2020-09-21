import datetime
import time
import psycopg2
from prettytable import PrettyTable
from termcolor import colored
from datetime import datetime, timedelta ,timezone



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
sql=(f'''SELECT task_number , task_name , task_time  FROM groundstation.sequencer_auto
''')
curr.execute(sql)
rows = curr.fetchall()



#print(date_now)

col_names = []

#date1=date(4:25:41.500101)


dt = datetime(2010, 2, 25, 23, 23)
dr=time.mktime(dt.timetuple())

#print('type dt', type(dt))
#print(dr)
while True:
    x = PrettyTable(['task_number','task_name','task_date','remaining_time'])
    date_now = datetime.now()
    for elt in rows:

        elt_unix_time = time.mktime(elt[2].timetuple())
        date_nowg = time.mktime(date_now.timetuple())
        remaining_time = elt_unix_time - date_nowg
        #print(remaining_time)
        #print('type delta',type(time_delta))
        #time.mktime(time_delta.timetuple())
        #time_delta2=   elt[2] - time.ctime()
        tab=[elt[0],elt[1],elt[2],remaining_time]


        x.add_row(tab)
        #x.add_row(time_delta)

    print(x.get_string())

    time.sleep(5)


'''
while True:
    print("slm")


    time.sleep(3)

'''
#t1 = threading.Thread(target=insert_line_dict, args=(sequence_task,))
#t1.start()      # starting thread 1

