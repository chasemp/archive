#!/usr/bin/env python

"""
2009 Chase Pettet

This script controls and shows status information for sites loadbalanced through LVS.

"""
import subprocess, os, sys, re, signal
from lvs_dicts import *
from optparse import OptionParser
from format_columns import *


def runBash(cmd):
 """
 Runs a command in the Bash shell and returns output
 """
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 out = p.stdout.read().strip()
 return out

def get_args():
 """
 Gets arguments from the user at the CLI and translates them into values.
 """

 global website, group, action, server, port, usage, filter
 usage = """\n

               Websites (-w) : mysite
               Actions (-a) : show, stats, up, down, sleep and unsleep.
               Servers (-s): server101, server102, server103
               Site groups (-g): lb, testlb, and xtest
               Protocols (-p): 80 and 443 (default is 443 for show/stats, 443 and 80 for sleep/unsleep/up/down)
               Filter (-f): any Server. Only available with 'stats' action.  Multiple servers can be separated by commas.

               Ex.

               Show stats on all sites in 'lb' group:                          %s -a stats -g lb

               Show stats on lb group filtered by Server:                      %s -a stats -g lb -f server101 (multiple servers: -f server101,server102,server103)

               Show stats for 'webservices' only in 'lb' group:                %s -a show -g lb -w webservices

               Sleep 'webservices' for group 'testlb' on 'server001':             %s -a sleep -g testlb -w webservices -s server101

               Unsleep 'webservices' for group 'testlb' on 'server001':           %s -a unsleep -g testlb -w webservices -s server101

               Remove 'server001' from 'testlb' pool for 'webservices':           %s -a down -g testlb -w webservices -s server101

               Add 'server001' from 'testlb' pool for 'webservices':              %s -a up -g testlb -w webservices -s server101


""" % (sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0], sys.argv[0])
 parser = OptionParser(usage)
 parser.add_option("-a", "--action", dest="action",
                   help="Action to take.  (show | up | down | sleep | unsleep)")
 parser.add_option("-g", "--group", dest="group",
                   help="Site group to perform action on.  (lb | testlb | xbeta)")
 parser.add_option("-w", "--website", dest="website",
                   help="Website to control.  (mysite)")
 parser.add_option("-s", "--server", dest="server",
                   help="Server to control.  (server101 | server102 | server103)")
 parser.add_option("-p", "--port", dest="port", default="443",
                   help="Port to show configuration for.  Defaults to 443. (443| 80)")
 parser.add_option("-f", "--filter", dest="filter", default="None",
                   help="Use '-f' with the stats action to group by Server.  (server101 | server102 | server103)")
 parser.add_option("-v", "--verbose",
                   action="store_true", dest="verbose")
 (options, args) = parser.parse_args()
 action = options.action
 website = options.website
 server = options.server
 port = options.port
 group = options.group
 filter = options.filter.swapcase()

class LVS_Site:
 """
 Defines a class to interact with LVS kernel through ipvsadm command line tool.
 """
 def show(self, site, proto):
   showsite = "ipvsadm -L -t %s:%s --sort" % (site, proto)
   showsiteresult = runBash(showsite)
   return showsiteresult

 def up(self, site, server):
   upsite_80 = "ipvsadm -a -t %s:%s -r %s:%s -w 1 -m" % (site, "80", server, "80")
   upsite_443 = "ipvsadm -a -t %s:%s -r %s:%s -w 1 -m" % (site, "443", server, "443")
   upsiteresult_80 = runBash(upsite_80)
   upsiteresult_443 = runBash(upsite_443)
   return upsiteresult_443

 def down(self, site, server):
   downsite_80 = "ipvsadm -d -t %s:%s -r %s:%s" % (site, "80", server, "80")
   downsite_443 = "ipvsadm -d -t %s:%s -r %s:%s" % (site, "443", server, "443")
   downsiteresult_80 = runBash(downsite_80)
   downsiteresult_443 = runBash(downsite_443)
   return downsiteresult_443

 def sleep(self, site, server):
   sleepsite_80 = "ipvsadm -e -t %s:%s -r %s:%s -w 0 -m" % (site, "80", server, "80")
   sleepsite_443 = "ipvsadm -e -t %s:%s -r %s:%s -w 0 -m" % (site, "443", server, "443")
   sleepsiteresult_80 = runBash(sleepsite_80)
   sleepsiteresult_443 = runBash(sleepsite_443)
   return sleepsiteresult_443

 def unsleep(self, site, server):
   unsleepsite_80 = "ipvsadm -e -t %s:%s -r %s:%s -w 1 -m" % (site, "80", server, "80")
   unsleepsite_443 = "ipvsadm -e -t %s:%s -r %s:%s -w 1 -m" % (site, "443", server, "443")
   unsleepsiteresult_80 = runBash(unsleepsite_80)
   unsleepsiteresult_443 = runBash(unsleepsite_443)
   return unsleepsiteresult_443

def signal_handler(signal, frame):
 """
 Gets arguments from the user at the CLI and translates them into values.
 """
 sname = os.path.split(sys.argv[0])[1]
 print "\n   %s stopped via ctrl+c signal!\n" % (sname)
 sys.exit(0)

def get_actionsite():
 """
 Uses the values of website and group from CLI to return the correct site ip
 """
 try:
   #get the site ip needed by looking looking up by (ex. getmybalance) and site type (ex. lb or testlb)
   actionsite = match_site[website]["%s" % (group)]
   return actionsite

 except:

  print "\nScript Error: Unable to get actionsite.  Are you providing a valid website '-w <Ex. webservices>' and a group '-g <Ex. lb>'?\n"
  print "\n" + usage
  sys.exit(1)


def get_actionserver():
 """
 Uses the values of website and server from CLI to return the correct server ip
 """
 try:

   #get the server ip needed by looking up by site (ex. getmybalance) and server (ex. server001)
   actionserver = match_site[website]["%s" % (server)]
   return actionserver

 except:

  print "\nScript Error: Unable to get actionserver.  Are you providing a valid website '-w <Ex. webservices>' and a server '-s <Ex. server001>'?\n"
  print "\n" + usage
  sys.exit(1)

def translate_results(modlines):
 """
 Takes input and swaps out text values for value key pairs defined by matches in a dictionary
 """
 regex_dict_master = {}

 for regex_dict in regex_dict_list:
   regex_dict_master.update(regex_dict)

 for k, v in regex_dict_master.iteritems():
   modlines = re.sub(k, v, modlines)

 return modlines

def translate_print_results_by_server(server_listing):
     """
     Takesouput and translates it and then reformats for server centric view of data
     """
     results_list = []
     print "\n"
     print FormatColumns(((7, LEFT), (10, CENTER), (25, CENTER),(7, CENTER), (7, CENTER), (7, RIGHT)),["Server", "Group", "Website", "Weight", "Active", "Inactive"])
     print "_______________________________________________________________________________" + "\n"

     for i in site_list:
       lbsite =  i[group]
       lbstats = site_instance.show(lbsite, port)
       mod_results = translate_results(lbstats)

       for item in server_listing:
         for line_split in mod_results.splitlines():
           if "TCP" in line_split:
             site_filter = line_split.split()
             group_filter = site_filter[1].strip()
             website_filter = site_filter[2].strip()
           if item in line_split:
             server_filter = line_split.split()
             host_filter = server_filter[0].strip()
             weight_filter = server_filter[2].strip()
             active_filter = server_filter[3].strip()
             inactive_filter = server_filter[4].strip()
             format_line = FormatColumns(((7, LEFT), (10, CENTER), (25, CENTER),(7, CENTER), (7, CENTER), (7, RIGHT)),[host_filter, group_filter, website_filter, weight_filter, active_filter, inactive_filter])
             formatted_string  = str(format_line)
             results_list.append(formatted_string)
     sorted_list = sorted(results_list)
     for item in sorted_list:
       print item + "\n"


def main():
 #define global variables defined in main()
 global site_list, site_instance
 #Set up script to handle quit signals
 signal.signal(signal.SIGINT, signal_handler)

 #parse arguments for processing
 get_args()

 #instantiate instace of LVS_Site to manipulate
 site_instance = LVS_Site()

 #provide a list of site dicts to loop through for stats
 site_list = [wsrv, gmba, admn, info, rprt, mgmt, slnk]

 if action == "stats":

   if filter.swapcase() == "None":

     for i in site_list:
       lbsite =  i[group]
       lbstats = site_instance.show(lbsite, port)
       mod_results = translate_results(lbstats)
       print ""
       print mod_results

   elif "," in filter:
     server_list = filter.split(',')
     translate_print_results_by_server(server_list)
   else:
     server_list = filter.split()
     translate_print_results_by_server(server_list)

 elif action == "show":
   actionsite = get_actionsite()
   mod_results = translate_results(site_instance.show(actionsite, port))
   print ""
   print mod_results

 elif action == "down":
   actionserver = get_actionserver()
   actionsite = get_actionsite()
   site_instance.down(actionsite, actionserver)
   mod_results = translate_results(site_instance.show(actionsite, port))
   print ""
   print mod_results

 elif action == "up":
   actionserver = get_actionserver()
   actionsite = get_actionsite()
   site_instance.up(actionsite, actionserver)
   mod_results = translate_results(site_instance.show(actionsite, port))
   print ""
   print mod_results

 elif action == "sleep":
   actionserver = get_actionserver()
   actionsite = get_actionsite()
   site_instance.sleep(actionsite, actionserver)
   mod_results = translate_results(site_instance.show(actionsite, port))
   print ""
   print mod_results

 elif action == "unsleep":
   actionserver = get_actionserver()
   actionsite = get_actionsite()
   site_instance.unsleep(actionsite, actionserver)
   mod_results = translate_results(site_instance.show(actionsite, port))
   print ""
   print mod_results

 else:
   print "\nunknown or incorrect options!\n"
   print usage
 print ""

if __name__ == '__main__':
          main()
