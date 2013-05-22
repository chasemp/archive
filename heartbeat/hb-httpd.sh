#!/bin/sh
#

service=httpd

case $1 in
start)
       for name in $service ; do
               statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
                       then
                               /etc/init.d/httpd start
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

       for name in $service ; do
               statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
                       then
                               echo "DOWN $name is already stopped"
                               exit 0
                       else
                              /etc/init.d/httpd stop
                              for name in $service ; do
                              statq=$(/bin/ps -C $name |/bin/grep -n 0)
                                    if [ -z "$statq" ]
                                    then
                                          echo "DOWN $name is stopped"
                                          exit 0
                                    else
                                          echo "OK $name is still running"
                                          exit 1
                              fi ; done
       fi ; done



       ;;
status)
       for name in $service ; do
       statq=$(/bin/ps -C $name |/bin/grep -n 0)
               if [ -z "$statq" ]
               then
                       echo "DOWN $name is stopped"
                       exit 0
               else
                       echo "OK $name is running"
                       exit 0
       fi ; done
       ;;
*)
       echo "Syntax incorrect.  You need {start|stop|status}"
       ;;
esac
