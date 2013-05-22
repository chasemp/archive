#!/bin/bash
#2009 Chase Pettet
#This script should be used on a Heartbeat host that is standalone
#
STATEB4=$(drbdadm state opt_r0)
echo "sleeping..."
sleep 10
wall "The current DRBD status is $STATEB4"
logger "The current DRBD status is$STATEB4"
drbdadm primary all
STATEA4=$(drbdadm state opt_r0)
wall "After drbdadm primary all the DRBD status is $STATEA4"
logger "After drbdadm primary all the DRBD status is $STATEA4"
sleep 5
logger "Attemping to mount DRBD /dev/drbd0"
wall "Attemping to mount DRBD /dev/drbd0.."
mount /dev/drbd0 /opt
sleep 2
STATEMNT=$(mount -l | grep /dev/drbd0)
wall "Mount status of /dev/drbd0 $STATEMNT"
logger "Mount status of /dev/drbd0 $STATEMNT"
sleep 10
#INSERT ANY SERVICES THAT RELAY ON DRBD DISK DATA BELOW THIS POINT

exit 0
