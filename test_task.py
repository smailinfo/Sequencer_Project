
import os
import sys





print(sys.argv[1] , sys.argv[2])
def check_host(hostname:str=''):
    try:
        response = os.system("ping -w3 " + hostname + "  > /dev/null  ")
        if response == 0:
            response='terminated OK'
            print (hostname, 'is up! \n ')
            with open(f'/home/cgs/PycharmProjects/Sequencer/Files/act_{sys.argv[1]}_{sys.argv[0]}.txt', 'a') as f:
                f.write(f"task_name {response}")

        else:
            print(hostname, 'is down! \n ')
            response = 'terminated NOK'
            with open(f'/home/cgs/PycharmProjects/Sequencer/Files/act_{sys.argv[2]}_{sys.argv[1]}.txt', 'a') as f:
                f.write(f"\ntask_name {response}")

    except Exception as e :
        print((f' the task is not finshed because{e}'))
        with open(f'/home/cgs/PycharmProjects/Sequencer/Files/log.txt', 'w') as f:
            f.write(f'the task is not finshed because{e}')

check_host('192.168.148.111')
print ('Just I test this script .... ')