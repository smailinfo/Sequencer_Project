import datetime
from ftplib import FTP

ftp = FTP(host="192.168.148.132", user="sccope",passwd="sccope")
ftp.cwd("/EXCHANGE/Internal/FDS/SCC")
file_name = sorted(ftp.nlst('PLANPASS_ALS2A*.asc'))
print(len(file_name))
for i in file_name:
    pass
print(i)