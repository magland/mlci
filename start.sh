#!/bin/bash

trap 'kill %1; kill %2;' SIGINT

python3 mlstatus/run_mlstatus.py &
kbucket-host output --auto

