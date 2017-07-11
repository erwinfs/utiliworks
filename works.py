# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#This is a simple web service that finds and returns the nearest street Works
#that are contained in a '|' delimeted file works.txt
#There is also a web service for downloading works.txt from an Object Store
#/ape/download

import os
from flask import Flask, jsonify
#Use CORS to make API available to any client
#https://pypi.python.org/pypi/Flask-Cors/3.0.3
#from flask_cors import CORS, cross_origin

import math
import csv
import json
import swiftclient
import cfg

#Specify filename and container name to get file out of Object Storage
file_name = "works.txt"
cont_name = "works"

#Credentials for object storage
auth_url = cfg.auth_url
project = cfg.project
project_id =  cfg.project_id
region= cfg.region
user_id= cfg.user_id
username= cfg.username
password= cfg.password
domainId= cfg.domainId
domainName= cfg.domainName
role= cfg.role

def toRadians(d):
    r = d * math.pi / 180.0
    #print('toRadians', d, r)
    return r

#Calculate the distance as the crow flies between any two points
def distance(lat1, lon1, lat2, lon2):
    #print('distance',lat1, lon1, lat2, lon2)
    R = 6371000.0 #Radius of the earth in m
    dLat = toRadians(lat2-lat1) #functions in radians
    dLon = toRadians(lon2-lon1)
    rlat1 = toRadians(lat1)
    rlat2 = toRadians(lat2)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(rlat1) * math.cos(rlat2) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c    #Distance in m
    return d

app = Flask(__name__)

#Use CORS to make this service public
#CORS(app)

#Use this to display the HTML / Javascript front end
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

#Use this to download a file from object storage
@app.route('/api/download/', methods=['Get'])
def downloadFile():
    #Create object storage object
    conn = swiftclient.Connection(key=password,
    authurl=auth_url,
    auth_version='3',
    os_options={
      "project": project,
      "project_id": project_id,
      "region_name": region,
      "user_id": user_id,
      "username": username,
      "password": password,
      "domainId": domainId,
      "domainName": domainName
    })
    sobj = conn.get_object(cont_name, file_name)
    with open(file_name, 'wb') as f:
	       f.write(sobj[1])

    print('Downloaded ' + file_name + ' from ' + cont_name)
    return jsonify ({'filename' : file_name, 'cont_name' : cont_name})

#Works web servie starts here
@app.route('/api/works/<latlon>', methods=['Get'])
def FindNearestWorks(latlon):

    lst = []
    #Read list of works from a delimeted file (use | as delimeter to prevent issues with commas)
    #wrkFile = csv.reader(open('works.csv'), delimiter = '|')
    wrkFile = csv.reader(open(file_name), delimiter = '|')
    for row in wrkFile:
        lst.append({'lat': row[0], 'lon': row[1], 'wrks': row[2]})

    #Strip latitude and longitude from url
    lat = float(latlon.split(',')[0])
    lon = float(latlon.split(',')[1])

    found = 0
    nearestDistance = 99999999.9

    #Loop through the list to works location that is closest to the supplied position
    for l in lst:
        d = distance( float(l['lat']), float(l['lon']), lat,  lon)
        if (d < nearestDistance):
            found += 1
            nearestDistance = round(d, 2)
            latWrk= round(float(l['lat']), 6)
            lonWrk= round(float(l['lon']), 6)
            wrkDescr = l['wrks']

    #Create python dictionary
    message = {'works': wrkDescr, 'lat': latWrk, 'lon': lonWrk, 'distance' : nearestDistance}
    print(message)

    #Convert Dictionary to json object. This could be done in return statement
    #This allows it to be printed to the console before it is returned
    retval = jsonify(message)
    print(retval)
    return retval

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
