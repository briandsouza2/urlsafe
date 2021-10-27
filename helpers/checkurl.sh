#!/bin/bash
# Checks the hostname_port and URI to see if it's blocked
HOSTNAME_PORT=$1
URI=$2
encoded_value=$(python3 -c "import urllib.parse; print (urllib.parse.quote('''$URI'''))")
set -x
curl "http://localhost:5000/urlinfo/1/${HOSTNAME_PORT}/$encoded_value"
