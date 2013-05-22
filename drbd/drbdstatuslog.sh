#!/bin/bash
#
#2009 Chase Pettet
#
#In The event of a DRBD split brain incident.  It is important to be able
#to find out historically which node was primary.  This script makes it relatively
#easy to do that by logging the state of HB and DRBD on each node every 5 minutes (needs to be run via cron).
#
#To investigate use the command: grep DRBDSTATUSLOG /var/log/messages
#Add to cron: 0,5,10,15,20,25,30,35,40,45,50,55 * * * * /usr/local/bin/drbdstatuslog
########################
#Variables
########################
#
hbstatus=$(cl_status rscstatus)
drbdstatus=$(grep st: /proc/drbd | cut -d: -f4 | cut -c 1-3)
host=$(uname -n)
#
########################
#
log.event ()
{
               logger DRBDSTATUSLOG-$host "Current Heartbeat Status: $hbstatus".
               logger DRBDSTATUSLOG-$host "Current DRBD Status: $drbdstatus".
}

log.event

exit 0
        
