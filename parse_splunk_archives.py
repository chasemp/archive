#!/usr/bin/env python
import sys, os, time, subprocess

def runBash(cmd):
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 out = p.stdout.read().strip()
 return out

for i in os.listdir(path_to_splunk_frozen):
 #Define Command to get size of file on disk
 get_size = "du -sh %s" % (i)

 size = runBash(get_size).split("db")[0]
 i = i.split('_')
 finish = i[1]
 start = time.localtime(int(i[2]))
 finish = time.localtime(int(i[1]))
 c = time.strftime('%Y, %b, %d, %H, %M, %S', start)
 d = time.strftime('%Y, %b, %d, %H, %M, %S', finish)
 print "Size:",size,c,"--> ",d,"      ",i
#  print c,"--> ",d,"    ",i
#  print "Begins: %s and Ends: %s" % (a, b)

