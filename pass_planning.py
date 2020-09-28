#################################################################################
#
#
#
#
#
#
##################################################################################


from datetime import datetime
import time
import psycopg2
import sys
from prettytable import PrettyTable
import re
from ftplib import FTP
from configparser import SafeConfigParser , ConfigParser
from termcolor import colored
from tqdm import tqdm
from alive_progress import alive_bar
import os , fnmatch
import glob

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
    file_name_2a = configure.get(section2,'file_name1')
    file_name_2b = configure.get(section2, 'file_name2')
    located_path = configure.get(section2,'located_path')

    files_list=[file_name_2a,file_name_2b]
    if check_host(hostname)=='OK':
        try:
            ftp = FTP(hostname)
            ftp.login(usr, pwd)
            ftp.cwd(path)
            print(ftp.pwd())

            for file in files_list:
                files = sorted(ftp.nlst(file+'*.asc'))
                for f in files:
                    pass
                print(f)
                my_file = open(located_path + "/" + f, 'wb')  # Open a local file to store the downloaded file
                ftp.retrbinary('RETR ' + f, my_file.write, 1024)  # Enter the filename to download
                print(colored(f" '{f}' : file transfert  completed with success \n ", "green"))
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
            if  x[0] >=6  and x[0]<=k :
                #if x[1].find() ....
                #print(x[0], x[1])
                pass_list.append(x[1] )
    #for i in pass_list :
      #  print(i)
    return pass_list


def extract_pass_2a(pass_planing_file):
    pass_list_2a = []

    with open(pass_planing_file) as infile:
        if 'A2ORAN' in infile.read():
            sta = 101
        if 'A2OUAR' in infile.read():
            sta = 100
        else:
            sta = 000
            print('please check your file station id !!! ')


    pass_list=extract_line(pass_planing_file)
    with alive_bar(len(pass_list)) as bar:
        print(" ********* Start extracting ********* ")
        if re.findall("ALS2A", pass_planing_file):
            for i in pass_list:
                #date_beg=i[1:11]
                #time_beg=i[12:20]
                #date_end = i[26:36]
                #time_end = i[37:45]
                duration=i[52:57]
                date_begining = i[1:20]
                date_ending = i[26:45]
                #date_beg = datetime.strptime(date_beg, "%Y/%m/%d")    # convert str to date
                #date_beg = datetime.strftime(date_beg, "%d/%m/%Y")    # # convert time to  str
                pass_2a= 938, "ALSAT2A" , date_begining , date_ending , duration , sta
                pass_list_2a.append(pass_2a)

                #print(date_beg , time_beg , date_end , time_end , duration )
                bar()
                time.sleep(0.01)

        if re.findall("ALS2B", pass_planing_file):
            for i in pass_list:
                # date_beg=i[1:11]
                # time_beg=i[12:20]
                # date_end = i[26:36]
                # time_end = i[37:45]
                duration = i[52:57]
                date_begining = i[1:20]
                date_ending = i[26:45]
                # date_beg = datetime.strptime(date_beg, "%Y/%m/%d")    # convert str to date
                # date_beg = datetime.strftime(date_beg, "%d/%m/%Y")    # # convert time to  str
                pass_2a = 939, "ALSAT2B", date_begining, date_ending, duration, sta
                pass_list_2a.append(pass_2a)

                # print(date_beg , time_beg , date_end , time_end , duration )
                bar()
                time.sleep(0.01)


    print(colored(f"\nfile:{pass_planing_file} "),colored("is extracted \n" , "green"))
    return pass_list_2a


def delete_from_table(schema:str='',table_name:str=''):
    coonn = connexion()
    curr = coonn.cur
    curr.execute(f'delete from {schema}."{table_name}" ')
    coonn.commit()


def file_browser(file_name,located_path):
    if  glob.glob(located_path+'/'+file_name):
        for f in sorted(glob.glob(located_path + '/' + file_name)):
            pass
        return f
    else :
        print(colored(f'file {file_name} is not exist .... ',"red") )







def save_pass(section:str=''):

    file_name_2a = configure.get(section,'file_name1')
    file_name_2b = configure.get(section, 'file_name2')
    located_path = configure.get(section , 'located_path')
    #print(file_name_2a,file_name_2b)
    #print(located_path)
    file_name = [file_browser(file_name_2a,located_path),file_browser(file_name_2b,located_path)]
    #file_browser(file_name_2a, located_path)

    schema='groundstation'
    table_name='planning_pass'
    col_value_dict = {
        'sat_id': '',
        'sat_name': '',
        'AOS': '',
        'LOS': '',
        'Duration': '',
        'station_id': '',
    }

    coonn = connexion()
    curr = coonn.cur
    delete_from_table(schema, table_name)
    columns = list(col_value_dict.keys())
    #values = list(col_value_dict.values())  # liste append

    for f in file_name:
        print(f)
        values = extract_pass_2a(f)
        try:
            with alive_bar(len(values)) as bar:
                c = 0
                for p in values:
                    print(p)
                    # print(list(p ))
                    sql = (f'INSERT INTO {schema}."{table_name}" ("' + '", "'.join(
                        ['%s'] * len(columns)) + '"' + ") ") % tuple(
                        columns) + "VALUES (" + ", ".join(["%s"] * len(columns)) + ")"
                    curr.execute(sql, list(p))
                    coonn.commit()
                    c += 1
                    bar()
                    time.sleep(0.01)
                print(colored(f"{c}:", "green"), ("pass are saved \n "))

        except Exception as e:
            print(colored(f'any pass is not  saved  because {e} \n ', "red"))

    print("*********  New planing pass list ********* \n  ")
    pass_existing()

    #for file in file_name:
       # values = extract_pass_2a(located_path+"/"+file_name)
    #for i in values:
        #print (i)

   


def pass_existing():
    coonn = connexion()
    curr = coonn.cur
    sql2=(f'''SELECT * FROM groundstation.planning_pass
    order by  planning_pass."AOS" asc limit 100
    ''')

    curr.execute(sql2)
    rows = curr.fetchall()
    list_time_pass=[]
    x = PrettyTable(["sat_id", "sat_name", "AOS", "LOS", "Duration","station_id"])
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
    #station = input("Please , choose one Station :  ORAN or OUAR \n")
    station = 'ORAN'
    if station=='ORAN':
        get_ftp('sccsrvnom2','PASS_FILE_O')
        #file_browser('PLANPASS*','/home/cgs/PycharmProjects/Sequencer/Files')
        save_pass('PASS_FILE_O')
        #extract_pass_2a('/home/cgs/PycharmProjects/Sequencer/Files/PLANPASS_ALS2B_20200926132210_MANUEL.asc')

    elif station=='OUAR':
        get_ftp('STATION_OUAR','PASS_FILE_OUAR')
        save_pass('PASS_FILE_OUAR')
    else :
        print('your station name is incorrect !!! \n  ')
        main()


if __name__ == '__main__':
    main()

    #pass_existing()











