#!/bin/bash

echo 52.58.196.119 dev-z912l6w0.eu.auth0.com > /etc/hosts
./manage.py migrate --no-input
./manage.py migrate --database=mongo --no-input
./manage.py runserver 0.0.0.0:8000