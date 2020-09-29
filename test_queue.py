
    with open (f'Files/act_{task_name}_{number_task}.txt','w') as f:
        f.write(f"""##################################################################################
#  Suivi de passage bande S 
#  Sequencer Version        = 0.1
#  System configuration     = /home/cgs/PycharmProjects/Sequencer/tasks.ini
#  Generation Time    = {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
##################################################################################
""")

        f.write(f"\ntask_name= {task_name}\ntask_time= {time_task}\ntask_number= {number_task}\nsat_name= {line_value_dict['sat_name']}\nsat_id= {line_value_dict['sat_id']}\nstatus= {line_value_dict['status']}\nfile_name= act_{task_name}_{number_task}.txt")

