#Simple python script to upload ./data/works.txt to object storage
#and then call /api/download to download the file to the web server
#for both loacal and bluemix server, ensure that both are running !

import swiftclient
import urllib.request

#Specify filename and container name to get file out of Object Storage
file_nameSrc = "works_src.txt"
file_name = "works.txt"
cont_name = "works"

#Credentials for object storage
auth_url = "https://lon-identity.open.softlayer.com/v3"
project = "object_storage_1b885008_464c_43d5_9dc1_fbe603a79525"
project_id =  "4a9ca921887640639289c818531bd517"
region= "london"
user_id= "e1a1ab03073d4fa3ba8ee2d68be42f5a"
username= "admin_5127cf3f164c4012f377599cb658584de59aca5c"
password= "I!=dt-BPf3.^6fCg"
domainId= "6543fe3416ae4d13b26c96ac415e0535"
domainName= "1390751"
role= "admin"

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


with open(file_nameSrc, 'r') as upload_file:
	conn.put_object(cont_name, file_name, contents= upload_file.read())

urllib.request.urlopen('http://localhost:5000/api/download/')
urllib.request.urlopen('https://efs-utiliworks.eu-gb.mybluemix.net/api/download/')
