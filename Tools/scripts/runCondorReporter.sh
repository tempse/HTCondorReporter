#!/bin/bash

echo "Starting nohup with condorReporter..."
nohup krenew -t -K 10 -- bash -c "condorReporter.py" &
