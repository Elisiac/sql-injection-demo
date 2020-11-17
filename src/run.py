#!env/bin/python3
from app import flaskapp

flaskapp.run(host="0.0.0.0", threaded=True, debug=True)
