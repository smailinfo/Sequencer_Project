#Open the ISS TLE file
tlefile=open('ISS.txt', 'r').read()
#Split the TLE data into a ephem readable format.
tlesplit=tlefile.split('\n')
#Analyse the split data.
tle_rec = ephem.readtle(tlesplit[0], tlesplit[1], tlesplit[2])
tle_rec.compute()
#Convert the sub satellite value (lat) to a string, then into DDMMSS format.
DMSsublatS="%s" %tle_rec.sublat
DMSsublat=DMSsublatS.split(':')
Dlat=int(DMSsublat[0])
Mlat=int(DMSsublat[1])
Slat=int(float(DMSsublat[2]))
DMSsublatsum=Dlat+Mlat/60+Slat/3600
#Convert the sub satellite value (lon) to a string, then into DDMMSS format.
DMSsublonS="%s" %tle_rec.sublong
DMSsublon=DMSsublonS.split(':')
Dlon=int(DMSsublon[0])
Mlon=int(DMSsublon[1])
Slon=int(float(DMSsublon[2]))
DMSsublonsum=Dlon+Mlon/60+Slon/3600