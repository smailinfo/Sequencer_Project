from datetime import datetime
import time
import psycopg2
import sys

from pip._vendor.requests import Timeout
from termcolor import colored
from prettytable import PrettyTable
import re
from ftplib import FTP
from configparser import SafeConfigParser , ConfigParser
from termcolor import colored
from tqdm import tqdm
from alive_progress import alive_bar
import os

configure = ConfigParser()
configure.read('sequencer.ini')


def check_host(hostname:str=''):

    response = os.system("ping -w3 " + hostname + "  > /dev/null  ")
    if response == 0:
        response='OK'
        print (hostname, 'is up!\n')

    else:
        print(hostname, 'is down!\n')
        response = 'NOK'
    return response


def get_ftp(section1,section2):                         # TODO : Time out   2 times
    #print(configure.sections())
    #print(configure.get('STATION', 'password'))

    hostname = configure.get(section1,'hostname')
    usr = configure.get(section1,'user')
    pwd = configure.get(section1,'password')
    path = configure.get(section2,'path')
    file_name = configure.get(section2,'file_name')
    located_path = configure.get(section2,'located_path')
    date1 = ''
    date2 = ''

    if check_host(hostname)=='OK':
        try:
            ftp = FTP(hostname)
            ftp.login(usr, pwd)
            ftp.cwd(path)
            # print(ftp.pwd())
            files = ftp.nlst()
            # print(files)

            if date1 == '':  # self.checkBox_without_date.isChecked():
                for f in files:
                    if file_name in f:
                        my_file = open(located_path + "/" + f, 'wb')  # Open a local file to store the downloaded file
                        ftp.retrbinary('RETR ' + f, my_file.write, 1024)  # Enter the filename to download
                        print(colored(" file transfert completed with success \n ", "green"))
            else:

                debut = datetime.strptime(date1, "%d/%m/%Y")  # convert str to time
                arret = datetime.strptime(date2, "%d/%m/%Y")

                while debut <= arret:
                    date_file = datetime.strftime(debut, "%Y_%m_%d")  # convert time to str

                    # print(date_file)
                    for f in files:
                        if file_name in f:
                            if date_file in f:
                                print(f)
                                my_file = open(located_path + "/" + f,
                                               'wb')  # Open a local file to store the downloaded file
                                ftp.retrbinary('RETR ' + f, my_file.write, 1024)  # Enter the filename to download

                    debut += datetime.timedelta(days=1)
                # my_file.close()
        except Exception as e:
            print(colored(f"file transfert failed because {e} \n ", "red"))



    elif check_host(hostname)=='NOK' :
        print (colored(f"No connection with {hostname} \n ","red"))


class connexion:
    try:
        def __init__(self):
            self.con=psycopg2.connect(database="alsat_2a", user="postgres" , password="cgs", host="localhost" , port="5432")
            self.cur=self.con.cursor()

        print(colored("Database opened with successufully\n ","green"))

        def close(self):
            self.close=self.con.close()
        def commit(self):
            self.com = self.con.commit()
    except Exception as e :
        print(colored(f" Access denided because {e} \n ","red"))


def extract_line(pass_planing_file):

    with open(pass_planing_file) as infile:
        for j in enumerate(infile):
            pass
    k=j[0]
    #print(k)
    pass_list=[]
    with open(pass_planing_file) as infile:
        for x in enumerate(infile):
            if  x[0] >=7  and x[0]<k :
                #if x[1].find() ....
                #print(x[0], x[1])

                pass_list.append(x[1][0:31] )

    return pass_list


def extract_pass_2a(pass_planing_file):
    pass_list_2a = []

    with open(pass_planing_file) as infile:
        if 'A2ORAN' in infile.read():
            sta = 101
        else:
            sta = 100

    pass_list=extract_line(pass_planing_file)
    with alive_bar(len(pass_list)) as bar:
        print(" ********* Start extracting ********* ")
        for i in pass_list:
            if re.findall("ALS2A", i) :
                date_2a=i[0:10]
                time_2a=i[11:19]
                duration_2a=i[20:25]
                date_2a = datetime.strptime(date_2a, "%Y/%m/%d")
                date_2a = datetime.strftime(date_2a, "%d/%m/%Y")
                date_pass_2a= sta ,938, "ALSAT2A" , date_2a +" "+ time_2a , duration_2a
                pass_list_2a.append(date_pass_2a)
                bar()
                time.sleep(0.01)

            elif re.findall("ALS2B", i):
                date_2a=i[0:10]
                time_2a=i[11:19]
                duration_2a=i[20:25]
                date_2a = datetime.strptime(date_2a, "%Y/%m/%d")
                date_2a = datetime.strftime(date_2a, "%d/%m/%Y")
                date_pass_2a= sta , 939 , "ALSAT2B" , date_2a +" "+ time_2a , duration_2a
                pass_list_2a.append(date_pass_2a)
                bar()
                time.sleep(0.01)

    print(colored(f"\nfile:{pass_planing_file} "),colored("is extracted \n" , "green"))
    return pass_list_2a


def delete_from_table(schema:str='',table_name:str=''):
    coonn = connexion()
    curr = coonn.cur
    curr.execute(f'delete from {schema}."{table_name}" ')
    coonn.commit()


def save_pass(section:str=''):
    file_name = configure.get(section, 'file_name')
    located_path = configure.get(section , 'located_path')
    #print (file_name,located_path)

    schema='groundstation'
    table_name='planing_pass'
    col_value_dict = {
        'station_id':'',
        'sat_id': '',
        'sat_name': '',
        'AOS': '',
        'pass_time': ''
    }

    coonn = connexion()
    curr = coonn.cur
    delete_from_table(schema, table_name)
    columns = list(col_value_dict.keys())
    #values = list(col_value_dict.values())  # liste append
    values = extract_pass_2a(located_path+"/"+file_name)
    #print (values)

    try:
        with alive_bar(len(values)) as bar:
            c=0
            for p in values:
                #print(p[3])
                #print(list(p ))
                sql = (f'INSERT INTO {schema}."{table_name}" ("' + '", "'.join(
                    ['%s'] * len(columns)) + '"' + ") ") % tuple(
                    columns) + "VALUES (" + ", ".join(["%s"] * len(columns)) + ")"
                curr.execute(sql, list(p))
                coonn.commit()
                c+=1
                bar()
                time.sleep(0.01)
            print(colored(f"{c}:" ,"green" ), ("pass are saved \n "))
            print("*********  New planing pass list ********* \n  ")
            #pass_existing()
    except Exception as e :
        print (colored(f'any pass is not  saved \n ' , "red"))


def pass_existing():
    coonn = connexion()
    curr = coonn.cur
    sql2=(f'''SELECT * FROM groundstation.planing_pass
    order by  planing_pass."AOS" asc limit 100
    ''')

    curr.execute(sql2)
    rows = curr.fetchall()
    list_time_pass=[]
    x = PrettyTable(["Station_ID", "Satellite_ID",  "Satellite", "Pass_Date", "Duration"])
    for i in rows:
        x.add_row(i)
        pass
        #print (i[3])
        #for j in i:
          #  d=datetime.strftime(j, "%Y/%m/%d")
           # t=datetime.strftime(j, "%H:%M:%S")
          #  print(d,t)
        list_time_pass.append(i[3])
    #print (list_time_pass)
    print(x.get_string())




def main():
    station = input("Please , choose one Station :  ORAN or OUAR \n")
    if station=='ORAN':
        get_ftp('STATION_ORAN','PASS_FILE_ORAN')
        save_pass('PASS_FILE_ORAN')

    elif station=='OUAR':
        get_ftp('STATION_OUAR','PASS_FILE_OUAR')
        save_pass('PASS_FILE_OUAR')
    else :
        print('your station name is incorrect !!! \n  ')
        main()


if __name__ == '__main__':
    main()

    #pass_existing()











