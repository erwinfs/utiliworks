# Python Flask Hello World Sample

This application demonstrates a simple, reusable Python web application based on the [Flask microframework](http://flask.pocoo.org/).
It uses an HTML function from javascript to retrieve the location of the user, calls a web service implemented in Python.
The output is displayed on an OSM map using v4 of the OSM Javascript library.
The works are stored in a '|' delimited text file works_src.txt.
The Python script upload.py is used to copy the file to a bluemix object store (via the swift interface) as works.txt and call the /api/download/ web service to download the file to the root directory.

## Run the app locally

1. [Install Python][]
1. cd into this project's root directory
1. Run `pip install -r requirements.txt` to install the app's dependencies
1. Run `python works.py'
1. Access the running app in a browser at <http://localhost:5000>

[Install Python]: https://www.python.org/downloads/
