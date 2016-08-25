"""
Simple example of Flask providing REST services

To run this, change to the directory containing this file and type
(linux):

export FLASK_APP=web.py
export FLASK_DEBUG=1
python -m flask run

on windows:

set FLASK_APP=web.py
set FLASK_DEBUG=1
python -m flask run

This will start the service on http://localhost:5000. Point a browser there and you should receive back "Hello, world!"

"""
from flask import Flask, jsonify, request
import os
import os.path
import re

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/ls/<dirname>',methods=['GET'])
def dir(dirname):
    'list the files in a directory'
    #
    # get dir name and any args (make sure it is a
    # subdirectory of the current dir)
    #
    base = os.path.basename(dirname)
    mode = request.args.get('mode','short')
    pattern = request.args.get('match','.*')
    #
    # find the files in that directory
    # that match the supplied (or default) regex
    #
    try:
        regex = re.compile(pattern)
        files = [fn for fn in os.listdir(base) if regex.search(fn) is not None]
    except FileNotFoundError as e:
        return 'No file matching {} found in {}/'.format(pattern,base)
    #
    # ---- if mode = short, just return the filenames
    #
    if mode == 'short':
        return jsonify( {'files':files} )
    #
    # if mode = long, gather up other info on each file too
    #
    if mode == 'long':
        fileD = {}
        for fn in files:
            filename = os.path.join(base,fn)
            fileD[fn] = {'size':os.path.getsize(filename)}
        return jsonify( {'files':fileD} )
    #
    # if unknown mode, print an error
    #
    return 'unknown mode <{}>'.format(mode)


