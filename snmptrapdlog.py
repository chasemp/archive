#!/usr/bin/python
#incredibly hokey way to get snmptrap events
#the ASA IPS is crap and only outputs in 2 formats one of which is
#proprietary this brainchild got me through an emergency


import sys, syslog, subprocess, time, re, os

#This script is called by snmptrapd
#It is configured to parse and log events from devices and translate results from regex_dict

def runBash(cmd):
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 out = p.stdout.read().strip()
 return out

regex_dict = {'.1.3.6.1.4.1.9.9.383.1.1.4\s':"Host: ",
               '.1.3.6.1.4.1.9.9.383.1.2.1\s':"Severity: ",
               '.1.3.6.1.4.1.9.9.383.1.2.2\s':"Alarm Traits: ",
               '.1.3.6.1.4.1.9.9.383.1.2.3\s':"SigDetails: ",
               '.1.3.6.1.4.1.9.9.383.1.2.4\s':"Description: ",
               '.1.3.6.1.4.1.9.9.383.1.2.5\s':"ID: ",
               '.1.3.6.1.4.1.9.9.383.1.2.6\s':"Value3: ",
               '.1.3.6.1.4.1.9.9.383.1.2.7\s':"Version: ",
               '.1.3.6.1.4.1.9.9.383.1.1.3\s':"Hex: ",
               '.1.3.6.1.4.1.9.9.383.1.1.2\s':"Hex: ",
               '.1.3.6.1.4.1.9.9.383.1.2.16\s':"Attacker: ",
               '.1.3.6.1.4.1.9.9.383.1.2.12\s':"Value1: ",
               '.1.3.6.1.4.1.9.9.383.1.2.13\s':"Value2: ",
               '.1.3.6.1.4.1.9.9.383.1.2.21\s':"Backplane: ",
               '.1.3.6.1.4.1.9.9.383.1.2.25\s':"Risk Rating: ",
               '.1.3.6.1.4.1.9.9.383.1.2.42\s':"Threat Rating: ",
               '.1.3.6.1.4.1.9.9.383.1.2.9\s':"SummaryType ",
               '.1.3.6.1.4.1.9.9.383.1.2.8\s':"Summary ",
               '.1.3.6.1.2.1.1.3.0\s':"Trigger Time: ",
               '.1.3.6.1.6.3.1.1.4.1.0\s':"Trap OID: ",
               '.1.3.6.1.4.1.9.9.383.1.2.26\s':"Value4: ",
               '.1.3.6.1.4.1.9.9.383.1.2.27\s':"Value5: ",
               '.1.3.6.1.4.1.9.9.383.1.2.17\s':"Target: ",
               '.1.3.6.1.4.1.9.9.383.1.1.1\s':"Event ID "}

def translate_results(modlines):
 for k, v in regex_dict.iteritems():
   modlines = re.sub(k, v, modlines)
 return modlines


def log_line(line, file):
 filename = file
 file = open(filename, 'a')
 file.write(line)
 file.close()


def main():
 try:
   now = time.ctime()
   L = []
   log_line("%s\n" % (now) , "/var/log/splunk/ciscoasa.log")
   for line in sys.stdin:
     line_time = "%s" % (line)
     L.append(line)
   for item in L:
     item.split(" ")
     modlines = translate_results(item)
     log_line(modlines, "/var/log/splunk/ciscoasa.log")
   log_line("EVENT_END\n\n", "/var/log/splunk/ciscoasa.log")
 except:
   log_line("\nError: (%s) Failed to log Cisco IPS Event!\n\n" % (sys.argv[0]), "/var/log/splunk/ciscoasa.log")

main()
