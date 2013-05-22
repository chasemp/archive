#!/usr/bin/env python

import subprocess
import os
import sys
import getopt

#
#Where is snmpget on your system?
#
SNMPGET = "/usr/bin/snmpget"
#


"""
Copyright (c) 2009 Chase Pettet

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

def user_help():
 print """

 This script executes nagios plugins (or whatever) through netsnmp and returns
 the appropriate exit code to nagios based on the text returned.

 Example:

 In the snmpd.conf file on a monitored host:

 exec .1.3.6.1.4.1.2021.51 check_users /usr/local/bin/netsnmp_scripts/check_users -w 20 -c 30

 Checking from the nagios server:

 check_netsnmp_exec.py -H <hostip> -C public -o .1.3.6.1.4.1.2021.51.101.1

 Possible returned output:

 USERS OK - 1 users currently logged in |users=1;20;30;0 (snmpd.conf on host)

 (note: you need the check_users plugin for this to work.)

 This script requires snmpget from the net-snmp package.

"""

def usage():
     print """-H <hostip> -C <community> -o <oid>"""

def version():
 print sys.argv[0] + " version .01"

def getargs():
 try:

   options, args = getopt.getopt(sys.argv[1:], 'H:C:o::hv', ['Host=', 'community=', 'oid=','help', 'version'])

 except getopt.GetoptError:
   usage ()
   sys.exit(2)

 opts = {}

 for o, a in options:
   opts[o] = a

 if '-v' in opts or '--version' in opts:
   version()
   sys.exit(0)
 if '-h' in opts or '--help' in opts:
   user_help()
   sys.exit(0)

 if len(options) < 3:
   usage()
   sys.exit(2)

 if '-H' in opts or '--Host' in opts:
   host = opts.get('-H', opts.get('--Host'))
 if '-C' in opts or '--community' in opts:
   community = opts.get('-C', opts.get('--community'))
 if '-o' in opts or '--oid' in opts:
   oid = opts.get('-o', opts.get('--oid'))
 else:
   usage()
 pullcmd =  SNMPGET + " -c " +community + " -v 2c " + host + " " + oid
 return pullcmd

def runBash(cmd):
 p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
 out = p.stdout.read().strip()
 return out

def snmpcut(snmpreturn):
 snmpreturni = snmpreturn.index('"')
 ploutput = snmpreturn[snmpreturni:].strip('"')
 return ploutput

def output_eval(status):
 if "CRITICAL" in status:
   print status + " (snmpd.conf on host)"
   sys.exit(2)
 elif "WARNING" in status:
   print status + "(snmpd.conf on host)"
   sys.exit(1)
 elif "OK" in status:
   print status + " (snmpd.conf on host)"
   sys.exit(0)
 elif "Uptime" in status:
   print status + " (snmpd.conf on host)"
   sys.exit(0)
 else:
   print "UNKNOWN: Result not interpreted by script."
   sys.exit(4)

def main():
 uservalues = getargs()
 rawsnmpvalue = runBash(uservalues)
 newsnmpvalue = snmpcut(rawsnmpvalue)
 output_eval(newsnmpvalue)

if __name__ == '__main__':
          main()
