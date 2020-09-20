import datetime
import time
import psycopg2
from termcolor import colored
from datetime import datetime, timedelta


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
while True:
    date_now = datetime.now()
    for elt in rows:
        time_delta = elt[2] - date_now
        print(time_delta)

    time.sleep(5)
'''
while True:
    print("slm")


    time.sleep(3)

'''
#t1 = threading.Thread(target=insert_line_dict, args=(sequence_task,))
#t1.start()      # starting thread 1

