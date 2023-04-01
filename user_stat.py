import re
from operator import itemgetter
import csv

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

    sorted_stats = dict(sorted(user_stats.items()))
    
    with open('user_statistics.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Username', 'INFO', 'ERROR'])
    
        for username, counts in sorted_stats.items():
            writer.writerow([username, counts['INFO'], counts['ERROR']])

user_statistic("./syslog.log")