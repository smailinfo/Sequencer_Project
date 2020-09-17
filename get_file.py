import datetime
from ftplib import FTP
from configparser import SafeConfigParser , ConfigParser
from termcolor import colored

configure = ConfigParser()
configure.read('sequencer.ini')

def get_ftp(section,section2):
    #print(configure.sections())
    #print(configure.get('STATION', 'password'))
    hostname = configure.get(section,'hostname')
    usr = configure.get(section,'user')
    pwd = configure.get(section,'password')
    path = configure.get(section2,'path')
    file_name = configure.get(section2,'file_name')
    located_path = configure.get(section2,'located_path')
    date1 = ''
    date2 = ''

    try:
        ftp = FTP(hostname)
        ftp.login(usr, pwd)
        ftp.cwd(path)
        print(ftp.pwd())
        files = ftp.nlst()
        #print(files)

        if  date1=='' :        #self.checkBox_without_date.isChecked():
            for f in files:
                if file_name in f:
                    my_file = open(located_path + "/" + f, 'wb')  # Open a local file to store the downloaded file
                    ftp.retrbinary('RETR ' + f, my_file.write, 1024)  # Enter the filename to download
                    print(colored("file transfert completed with success ", "green"))
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

                # matching = [s for s in files if date_file in s]
                # print(matching)
                # files_selected.append(matching)
                debut += datetime.timedelta(days=1)
            # my_file.close()
    except Exception as e :
        print ( colored (f"You don't connect to the server because {e}",'red'))



get_ftp('STATION_ORAN','PASS_FILE_ORAN')