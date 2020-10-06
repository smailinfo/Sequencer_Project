
p=0
while p<100:
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
           where planifier."task_time_start" > now() at time zone 'utc'
           order by planifier."task_time_start"
           asc limit 5
           ''')
    curr.execute(sql)
    rows = curr.fetchall()
    date_now = datetime.now()
    date_now = time.mktime(date_now.timetuple())
    for row in rows :
        row_unix_time = time.mktime(row[2].timetuple())
        remaining_time = row_unix_time - date_now
        tab = [row[0], row[1], row[2], remaining_time]
        print(tab)

        if remaining_time == 0:
            print("OK........OK")
            break


    print(p)
    p+=1
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
           where planifier."task_time_start" > now() at time zone 'utc'
           order by planifier."task_time_start"
           asc limit 5
           ''')
    curr.execute(sql)
    rows = curr.fetchall()
    time.sleep(1)



###############################################################################################




p=0
while p<100:
    sql = (f'''SELECT task_number , task_name , task_time_start  FROM groundstation.planifier
           where planifier."task_time_start" > now() at time zone 'utc'
           order by planifier."task_time_start"
           asc limit 5
           ''')
    curr.execute(sql)
    row = curr.fetchone()

    date_now = datetime.now()
    date_now = time.mktime(date_now.timetuple())
    row_unix_time = time.mktime(row[2].timetuple())
    remaining_time = row_unix_time - date_now
    tab = [row[0], row[1], row[2], remaining_time]
    print(tab)



    print(p)
    p+=1

    time.sleep(1)
