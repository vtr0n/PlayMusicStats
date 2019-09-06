#!/bin/bash

sleep 10
./manage.py migrate --no-input
./manage.py migrate --database=mongo --no-input
./manage.py runserver 127.0.0.1:8000