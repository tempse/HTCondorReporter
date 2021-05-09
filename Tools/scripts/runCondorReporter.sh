#!/bin/bash

echo "Starting nohup with condorReporter..."
nohup krenew -t -K 10 -- bash -c "~/public/HTCondorReporter/Tools/scripts/condorReporter.py" &
