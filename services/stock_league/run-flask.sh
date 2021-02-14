#!/bin/sh

export FLASK_ENV="development"
python /usr/src/app/manage.py run -h 0.0.0.0
