#!/bin/sh
gunicorn urlsafe:app -w 1 --threads 10 -b 0.0.0.0:5000
