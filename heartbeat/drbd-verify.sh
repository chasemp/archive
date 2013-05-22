#!/bin/bash
#
FILE="/etc/cron.d/drbdverify"
case $1 in
start)
       if [ -e $FILE ]; then
               echo "Already OK"
       else
               touch $FILE
               echo "45 23 * * * drbdadm verify all" >> $FILE
                       if [ -e $FILE ]; then
                               echo "OK"
                       else
                               echo "Still DOWN creation failed."
                       fi
       fi
       ;;
stop)
       if [ -e $FILE ]; then
               rm -f $FILE
               if [ -e $FILE ]; then
                       echo "Failed: Status is still OK"
               else
                       echo "DOWN"
               fi
       else
               echo "DOWN status unknown"
       fi
       ;;
status)
       if [ -e $FILE ]; then
               echo "OK"
       else
               echo "DOWN"
       fi
       ;;
*)
       echo "Syntax incorrect.  You need {start|stop|status}"
