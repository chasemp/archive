#!/bin/sh
#

service=nagios

case $1 in
start)
       for name in $service ; do
               statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
                       then
                               /etc/init.d/nagios start
                                       for name in $service ; do
                                               statq=$(/bin/ps -C $name |/bin/grep -n 0)
                                               if [ -z "$statq" ]
                                               then
                                                       echo "DOWN $name is still not running"
                                                       exit 1
                                               else
                                                       echo "OK $name is running"
                                                       exit 0
                                       fi ; done
                       else
                               echo "OK $name is already running"
                               exit 0
               fi ; done
       ;;
stop)
       /etc/init.d/nagios stop
       printf "Pending procs: \n"
       state=$(ps aux | grep $service | grep -v grep | grep -v hb-nagios | wc -l)
       while [ "$state" != "0" ]
       do
               printf "$state "
               sleep 1
               state=$(ps aux | grep $service | grep -v grep | grep -v hb-nagios | wc -l)
       done

       printf "\n"
       for name in $service ; do
       statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
               then
                       echo "DOWN $name is not running"
                       exit 0
               else
                       echo "OK $name is running"
                       exit 1
       fi ; done
       ;;
status)
       for name in $service ; do
       statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
               then
                       echo "DOWN $name is stopped"
               else
                       echo "OK $name is running"
       fi ; done
       ;;
*)
       echo "Syntax incorrect.  You need {start|stop|status}"
       ;;
esac
