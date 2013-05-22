#!/usr/bin/env python
import sys, os, time, subprocess

def runBash(cmd):
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 out = p.stdout.read().strip()
 return out

logs = []
logs_parsed = []

f = open('/var/log/squid/access.log','r')
for event in f.read().split('\n'):
   logs.append(event.split('\n'))
f.close()

for events in logs:
    for event in events:
        print "\n"
        now = event.split()[0].strip().rstrip(".")
        print time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.localtime(float(now)))
        print event
