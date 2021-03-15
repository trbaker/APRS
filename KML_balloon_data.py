#! /Users/tbaker/opt/anaconda3/envs/cndaPyCharm_TRB/bin/python

#import my modules
from kmlTools import kml2csv

# import common modules
from bs4 import BeautifulSoup
from arcgis.gis import GIS
import datetime as dt
import requests
import urllib.parse

# SET VARS
server="https://k12.maps.arcgis.com"
username=""
password=""
gis=GIS(server,username,password)
counter=1
inputfile = "/Users/tbaker/Dropbox/python/pycharm_projects/K12scripts/APRS_balloon/balloon.kml"
url = 'http://legacy-snus.habhub.org/tracker/datanew.php?format=kml&amp;mode=1days'
repeatedFeatures=0
dbaseSkipWrite=False

#GET KML DATA FILE
req = requests.get(url, allow_redirects=False)
req = str(req.content)
open(inputfile, mode='w').write(req)
print(' ** Balloon kml updated *** \n\n')

#PROCESS and OUTPUT ###########################################
with open(inputfile, 'r') as f:
    soup = BeautifulSoup(f, features='lxml')
    for node in soup.select('folder'):
        try:
            list = kml2csv(node, counter)  # write function list back into local variable called list
            list
            print(' ')
            print('Processing: ', list[3])
            counter = list[0]
            dbaseSkipWrite = False  # used for repeat point checking below.
            # write to AGO
            search_result = gis.content.search("id:336a770c33864e19adad7b7fb0c56259")
            search_result[0]
            balloon_item = search_result[0]
            balloon_layers = balloon_item.layers
            balloon_layers
            balloon_flayer = balloon_layers[0]
            # CHECK to see if there is a LAT/LON match in dbase before posting
            mylat = list[1]
            mylong = list[2]
            # dig down to get feature set, feature service, features - and then compare
            balloon_fset = balloon_layers[0].query()
            balloon_features = balloon_fset.features
        except:
            print('something went wrong about line 56. the loop was continued anyway.')
            continue  # return to top of for loop if error occurs.
        print('\u2588', end='')
        #Clean redundant and test data. Then send to feature service
        for i in balloon_features: #loop over each feature in the current feature service
            if (str(i.get_value('lat')) == mylat and str(i.get_value('long')) == mylong):
                dbaseSkipWrite=True # set flag so record is not written

        if dbaseSkipWrite:  # True is set when test or redundant data are found
            print('Point already exists or is test data. ')
        else:
            # if dbaseSkipWrite is False:
            print(counter, '   ***** New record: ', list[3], 'ALT: ', list[4])
            new_data = {"attributes":
                            {"lat": list[2],
                             "long": list[1],
                             "name": list[3],
                             "altitude": list[4],
                             "data": list[5],
                             "comments": list[6],
                             "datetime": list[7],
                             "syspostdatetime": dt.datetime.now()},
                             "geometry": {"x": list[1], "y": list[2], "spatialReference": {"wkid" : 4326}}}
            sub=balloon_flayer.edit_features(adds=[new_data])
            # print('Submission status: ', sub)  # TURN ON FOR TROUBLE SHOOTING
            counter=counter+1
total=counter-1
print(' *** Script complete. New records added: ', total)