
import os

from termcolor import colored


def check_host(hostname:str=''):

    try:
        response = os.system("ping -w3 " + hostname + "  > /dev/null & ")
        if response == 0:
            response='terminated OK'
            print (hostname, 'is up! \n ')



        else:
            print(hostname, 'is down! \n ')
            response = 'terminated NOK'
        return response
    except Exception as e :
        print(colored(f' the task is not finshed because','red'))

check_host('192.168.148.111')
print ('Just I test this script .... ')