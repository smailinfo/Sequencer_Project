
import os

def check_host(hostname:str=''):

    response = os.system("ping -w3 " + hostname + "  > /dev/null & ")
    if response == 0:
        response='OK'
        print (hostname, 'is up! \n ')

    else:
        print(hostname, 'is down! \n ')
        response = 'NOK'
    return response


check_host('192.168.148.111')
print ('I just test this script .... ')