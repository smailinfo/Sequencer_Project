from datetime import datetime
import time
import psycopg2
import sys
from termcolor import colored
from prettytable import PrettyTable
import re


def create_database(self, db_name: str, custom_sql=''):
    try:
        conn = psycopg2.connect(dbname='postgres', user='postgres', host='localhost')
        conn.autocommit = True
        cur = conn.cursor()

        if custom_sql == '':
            # sql = f"DROP DATABASE IF EXISTS {db_name} "
            sql = f"CREATE DATABASE {db_name} WITH OWNER = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1"
        else:
            sql = custom_sql

        cur.execute(sql)
        # cur.execute(sql2)
        print(colored(f"Database '{db_name}' created with success.", 'green', attrs=['bold']))

    except Exception as e:
        print(colored(f"Can not create DATABASE '{db_name}' !!! {e}", 'red'))

class connexion:
    def __init__(self):
        self.con = psycopg2.connect(database="alsat_2a", user="postgres", password="cgs", host="localhost", port="5432")
        self.cur = self.con.cursor()

    print("Database opened with successufully")

    def close(self):
        self.close = self.con.close()

    def commit(self):
        self.com = self.con.commit()

def create_schmas(custom_sql=''):
    coonn = connexion()
    curr = coonn.cur

    schema_liste = ["groundstation", "space"]
    # schema_liste.append("groundstation")
    if custom_sql != '':
        sql = custom_sql
    else:
        for schema in schema_liste:
            sql = f"""create schema {schema} authorization postgres"""
            try:
                curr.execute(sql)
                coonn.commit()
                print(f" the schemas {schema} are created  ")
            except Exception as e:
                print(colored(f"can't create shemas {schema} {e} ", 'red'))

def create_table(schema: str = '', table_name: str = '', table_parameters=None, primary_key: str = '', custom_sql=''):
    coonn = connexion()
    curr = coonn.cur

    try:
        if custom_sql != '':
            sql = custom_sql
        else:
            sql = f""" create table "{schema}"."{table_name}" 
            ("""
            for column in table_parameters.keys():
                sql += f'\n"{column}" {table_parameters.get(column)},'

            if primary_key != '':
                sql += f'\nPRIMARY KEY ("{primary_key}") )\n'
            else:
                sql = sql[:-1] + ")"  # eliminate ',' and add ')'

            curr.execute(sql)
            coonn.commit()
            print(f" Table {schema}.{table_name} is created  ")

    except Exception as e:
        print(colored(f"""Can not create table "{schema}"."{table_name}" !!! {e}""", 'red'))

def definition_tables():
    tables_info_list = []
    '''
    tables_info_list.append({
        'schema': 'space',
        'table_name': 'APFtable',
        'primary_key': 'APF_id',
        'table_parameters':
            {
             'sat_id':'smallint  NULL',
             'satation': 'character varying  NULL',
             'APF_time': 'character varying  NULL',
             'EL': 'float',
             'AZ': 'float'

             }})


    tables_info_list.append({
        'schema': 'space',
        'table_name': 'Next_pass',
        'primary_key': '',
        'table_parameters':
            {'APF_id': 'serial',
             'sat_id': 'smallint NOT NULL',
             'satation': 'character varying NOT NULL',
             'APF_time': 'timestamp without time zone',
             'EL': 'float',
             'AZ': 'float'


             }})



    tables_info_list.append({
        'schema': 'groundstation',
        'table_name': 'task_status',
        'primary_key': 'task_number',
        'table_parameters':
            {
                'task_number': 'integer NULL',
                'task_name': 'character varying  NULL',
                'task_time': 'timestamp  NULL',
                'sat_name': 'character varying  NULL',
                'status': 'character varying  NULL'

            }})
            
    '''

    tables_info_list.append({
        'schema': 'groundstation',
        'table_name': 'planning_pass',
        'primary_key': '',
        'table_parameters':
            {
                'sat_id': 'smallint NOT NULL',
                'sat_name': 'character varying  NULL',
                'AOS': 'timestamp  NULL',
                'LOS': 'timestamp  NULL',
                'Duration': 'float',
                'station_id': 'smallint NOT NULL',



            }})


    for table_info in tables_info_list:
        # print(table_info)
        create_table(schema=table_info.get('schema'),
                     table_name=table_info.get('table_name'),
                     table_parameters=table_info.get('table_parameters'),
                     primary_key=table_info.get('primary_key'))

def select_table():
    coonn = connexion()
    curr = coonn.cur

    sql = (f'''SELECT planing_pass."AOS" FROM groundstation.planing_pass
    where planing_pass."AOS" > now() at time zone 'utc'
    order by  planing_pass."AOS" asc limit 100
    ''')
    curr.execute(sql)

    rows = curr.fetchall()
    # print(rows)
    for i in rows:
        # i=datetime.strptime(i, "%Y/%m/%d")     # convert str to time
        # i=datetime.strftime(i, "%Y/%m/%d")     # convert time to  str
        # print (i)
        for j in i:
            d = datetime.strftime(j, "%Y/%m/%d")
            t = datetime.strftime(j, "%H:%M:%S")
            print(d, t)

# create_database('','alsat_2a','')
# create_schmas(custom_sql='')
definition_tables()
# insert_line_dict()
# insert_line_list()
#columns_dictionary()

# extract_pass_2a()

