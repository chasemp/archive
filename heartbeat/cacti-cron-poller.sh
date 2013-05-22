#!/bin/bash
#
FILE="/etc/cron.d/cacti"
case $1 in
start)
       if [ -e $FILE ]; then
               echo "Already active OK"
       else
               touch $FILE
               echo "*/5 * * * *     cacti   php /var/www/cacti/poller.php &>/dev/null" >> $FILE
                       if [ -e $FILE ]; then
                               echo "OK Cacti cron status is active"
                       else
                               echo "DOWN status is unknown. File cannot be created."

                       fi
       fi
       ;;
stop)
       rm -f $FILE
               if [ -e $FILE ]; then
                       echo "WARNING: status is unknown.  File cannot be removed."
               else
                       echo "DOWN Cacti cron status is inactive."
               fi
       ;;
status)
       if [ -e $FILE ]; then
               echo "OK Cacti cron status is active."
       else
               echo "DOWN Cacti cron status is inactive."
       fi
       ;;
*)
       echo "Syntax incorrect.  You need {start|stop|status}"
       ;;
esac
