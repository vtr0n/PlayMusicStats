#!/bin/bash

sleep 10
./manage.py migrate --no-input
./manage.py migrate --database=mongo --no-input
./manage.py runserver 0.0.0.0:8000