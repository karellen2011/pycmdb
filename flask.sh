#!/bin/bash
cd /home/mfranke/flask-cmdb3
export FLASK_APP=cmdb.py
export FLASK_DEBUG=1
flask run --host=192.168.2.11 --port=5003

