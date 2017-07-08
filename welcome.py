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

import os
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin

import math
import csv
import json

def toRadians(d):
    r = d * math.pi / 180.0
    #print('toRadians', d, r)
    return r

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
CORS(app)

#Pert of original template - for reference
@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/myapp')
def WelcomeToMyapp():
    return 'Welcome again to my app running on Bluemix!'

@app.route('/api/people')
def GetPeople():
    list = [
        {'name': 'John', 'age': 28},
        {'name': 'Bill', 'val': 26}
    ]
    return jsonify(results=list)

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

#Work starts here
@app.route('/api/works/<latlon>', methods=['Get'])
def FindNearestWorks(latlon):
    # lst = [
    #     {'lat': 51.074365, 'lon': -0.797313, 'wrks': 'Liphook cable fault, estimated completion date 2 days'},
    #     {'lat': 50.942798, 'lon': -2.699348, 'wrks': 'Digging up Jeremys house - no completion time planned'}
    # ]
    lst = []
    #print('lst1',lst)
    wrkFile = csv.reader(open('works.csv'), delimiter = '|')
    for row in wrkFile:
        #print('row',row)
        lst.append({'lat': row[0], 'lon': row[1], 'wrks': row[2]})

    #print('lst2',lst)

    lat = float(latlon.split(',')[0])
    lon = float(latlon.split(',')[1])

    found = 0
    nearestDistance = 99999999.9
    #print(lat, lon, found, nearestDistance)

    for l in lst:
        #print(l['lat'])
        d = distance( float(l['lat']), float(l['lon']), lat,  lon)
        #print('d',d)
        if (d < nearestDistance):
            found += 1
            nearestDistance = round(d, 2)
            latWrk= round(float(l['lat']), 6)
            lonWrk= round(float(l['lon']), 6)
            wrkDescr = l['wrks']

    #print(latWrk)
    message = {'Works': wrkDescr, 'lat': latWrk, 'lon': lonWrk, 'distance' : nearestDistance}
    print(message)
    retval = jsonify(message)
    print(retval)
    return retval

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))
