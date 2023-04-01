#!/usr/bin/env python3
import re
from operator import itemgetter
import csv

errors = {}

def count_errors(logfile):
    """This function reads the syslog file and returns a dictionary with type of error as key and it's frequency as value."""
    with open(logfile, "r") as f:
        logdata = f.readlines()
    
    for line in logdata:
        pattern = r"ticky: ERROR ([\w ']*)"
        match = re.search(pattern, line)
        if match:
            error_message = match.group(1)
            if error_message in errors.keys():
                errors[error_message] += 1
            else:
                errors[error_message] = 1

    sorted_errors = dict(sorted(errors.items(), key=itemgetter(1), reverse=True))
    
    with open('error_message.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Error', 'Count'])

        for key, value in sorted_errors.items():
            writer.writerow([key, value])
    


user_stats = {}

def user_statistic(logfile):
    with open(logfile, "r") as f:
        logdata = f.readlines()
    
    for line in logdata:
        pattern = r"(INFO|ERROR) (.*) \((.*)\)$"
        match = re.search(pattern, line)
        if match:
            action = match.group(1)
            username = match.group(3)
            if username not in user_stats.keys():
                user_stats[username] = {"INFO": 0, "ERROR": 0}
            user_stats[username][action] += 1

    sorted_stats = dict(sorted(user_stats.items(), key=itemgetter(0)))
    
    with open('user_statistics.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'INFO', 'ERROR'])
    
        for username, counts in sorted_stats.items():
            writer.writerow([username, counts['INFO'], counts['ERROR']])

user_statistic("./syslog.log")
count_errors("./syslog.log")

