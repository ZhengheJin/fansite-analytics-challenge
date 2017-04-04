#!/usr/bin/env bash

# one example of run.sh script for implementing the features using python
# the contents of this script could be replaced with similar files from any major language

# I'll execute my programs, with the input directory log_input and output the files in the directory log_output
#python ./src/process_log.py ./log_input/log.txt ./log_output/hosts.txt ./log_output/hours.txt ./log_output/resources.txt ./log_output/blocked.txt
python ./src/e1.py ./log_input/log.txt ./log_output/hours_new.txt ./log_output/visit_analysis.txt
python ./src/e2.py ./log_input/log.txt ./log_output/top_failure.txt
