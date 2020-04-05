#!/bin/bash

set -e

wait_for_database.sh

# run server
manage.py runserver 0.0.0.0:8000
